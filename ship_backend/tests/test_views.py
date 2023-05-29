from parameterized import parameterized
from rest_framework import status

from shipments.models import Shipment, Product
from shipments.utils import CustomPagination
from tests.base import APITestBase
from tests.factories import ShipmentFactory, ProductFactory


class TestGetShippingList(APITestBase):
    view_url = '/api/shipping/'
    count_per_page = CustomPagination.page_size

    @classmethod
    def setUpTestData(cls):
        shippings_count = 15

        for ind in range(shippings_count):
            ShipmentFactory(title=f'title_{ind}')

    def test_get_all_first_page(self):
        shipping_count = Shipment.objects.count()
        self.assertGreater(shipping_count, self.count_per_page)

        response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data
        self.assertEqual(response_data['count'], shipping_count)
        self.assertEqual(response_data['total_pages'], shipping_count//self.count_per_page + 1)
        self.assertEqual(response_data['page_size'], self.count_per_page)
        self.assertEqual(response_data['page_number'], 1)
        self.assertIsNotNone(response_data['next'])
        self.assertIsNone(response_data['previous'])
        self.assertEqual(len(response_data['results']), self.count_per_page)

    def test_get_second_page(self):
        shipping_count = Shipment.objects.count()
        self.assertGreater(shipping_count, self.count_per_page)

        response = self.client.get(self.view_url + '?page=2')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data
        self.assertEqual(response_data['count'], shipping_count)
        self.assertEqual(response_data['total_pages'], shipping_count // self.count_per_page + 1)
        self.assertEqual(response_data['page_size'], self.count_per_page)
        self.assertEqual(response_data['page_number'], 2)
        self.assertIsNone(response_data['next'])
        self.assertIsNotNone(response_data['previous'])
        self.assertEqual(len(response_data['results']), shipping_count % self.count_per_page)

    def test_get_search(self):
        response = self.client.get(self.view_url + '?simple_search=le_0')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data
        self.assertEqual(response_data['count'], 1)
        self.assertEqual(response_data['total_pages'], 1)
        results = response_data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'title_0')

    def test_get_search_in_linked_title(self):
        product1 = ProductFactory(title='what im doing why')
        product2 = ProductFactory(title='something')
        ShipmentFactory(product=product1)
        ShipmentFactory(product=product2)

        response = self.client.get(self.view_url + '?simple_search=ing')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data
        self.assertEqual(response_data['count'], 2)
        results = response_data['results']
        self.assertEqual(len(results), 2)


class TestPostShipping(APITestBase):
    view_url = '/api/shipping/'

    def test_post_ok(self):
        self.assertEqual(Shipment.objects.count(), 0)
        body = {
            'title': 'Erebus',
            'status': 'published'
        }
        response = self.client.post(self.view_url, body)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Shipment.objects.count(), 1)
        response_data = response.data
        self.assertEqual(response_data['title'], body['title'])
        self.assertEqual(Shipment.objects.count(), 1)
        ship = Shipment.objects.get(id=response_data['id'])
        self.assertEqual(ship.title, body['title'])
        self.assertEqual(body['status'], 'published')

    @parameterized.expand(['wrong_status', 0])
    def test_post_wrong_status(self, wrong_status):
        self.assertEqual(Shipment.objects.count(), 0)
        body = {
            'title': 'Erebus',
            'status': wrong_status
        }
        response = self.client.post(self.view_url, body)
        self.assertContains(response, 'Not valid option.', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Shipment.objects.count(), 0)

    def test_post_with_product_ok(self):
        product = ProductFactory()
        self.assertEqual(Shipment.objects.count(), 0)
        body = {
            'title': 'Erebus',
            'product': product.id
        }
        response = self.client.post(self.view_url, body)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Shipment.objects.count(), 1)
        response_data = response.data
        self.assertEqual(response_data['title'], body['title'])
        self.assertEqual(Shipment.objects.count(), 1)
        ship = Shipment.objects.get(id=response_data['id'])
        self.assertEqual(ship.title, body['title'])
        self.assertEqual(ship.product, product)

    def test_post_with_product_not_exists(self):
        product = ProductFactory()
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Shipment.objects.count(), 0)
        body = {
            'title': 'Erebus',
            'product': product.id + 1
        }
        response = self.client.post(self.view_url, body)

        self.assertContains(response, 'object does not exist', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Shipment.objects.count(), 0)


class TestGetShippingDetail(APITestBase):
    view_url = '/api/shipping/'

    def test_get_ok(self):
        ship = ShipmentFactory(title='title_1')

        response = self.client.get(f'{self.view_url}{ship.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data
        self.assertEqual(response_data['title'], ship.title)
        self.assertEqual(response_data['id'], ship.id)

    def test_get_not_exist(self):
        ship = ShipmentFactory(title='title_1')
        wrong_id = ship.id + 100
        response = self.client.get(f'{self.view_url}{wrong_id}/')
        self.assertContains(response, 'Not found.', status_code=status.HTTP_404_NOT_FOUND)


class TestPatchShippingDetail(APITestBase):
    view_url = '/api/shipping/'

    def setUp(self):
        self.ship = ShipmentFactory(title='title_1', status=1)

        super().setUp()

    def test_patch_ok(self):
        data = {
            "status": "done"
        }
        response = self.client.patch(f'{self.view_url}{self.ship.id}/', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_ship = Shipment.objects.get(id=self.ship.id)
        self.assertEqual(updated_ship.status, 3)
        response_data = response.data
        self.assertEqual(response_data['id'], self.ship.id)
        self.assertEqual(response_data['status'], data['status'])

    def test_patch_product_not_exists(self):
        data = {
            "status": 987
        }
        response = self.client.patch(f'{self.view_url}{self.ship.id}/', data, content_type='application/json')
        self.assertContains(response, 'Not valid option.', status_code=status.HTTP_400_BAD_REQUEST)
        updated_ship = Shipment.objects.get(id=self.ship.id)
        self.assertEqual(updated_ship.status, 1)


class TestDeleteShippingDetail(APITestBase):
    view_url = '/api/shipping/'

    def setUp(self):
        self.ship = ShipmentFactory()

        super().setUp()

    def test_delete_ok(self):
        self.assertEqual(Shipment.objects.count(), 1)

        response = self.client.delete(f'{self.view_url}{self.ship.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Shipment.objects.count(), 0)
