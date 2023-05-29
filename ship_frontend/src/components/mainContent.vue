<template>
    <v-container class="mt-5 pa-5 bg-grey-lighten-3">
        <v-btn
            size="small" class="mr-1" color="orange-darken-3"
            @click.prevent=""
        >
            add new shipping
        </v-btn>

        <v-divider class="my-5"></v-divider>

      <shipmentsList/>

    </v-container>
</template>

<script>
import axios from 'axios';
import shipmentsList from "@/components/shipmentsList.vue";

export default {
    name: "shipment",
    components: {
        shipmentsList,
    },

    data() {
        return {
            pageSizes: [10, 50, 100],
            shipments: null,
            currentPage: 1,
            pageSize: 10,
            pageVisibleCount: 5,
            pageCount: 0,
            modalDelRecord: false,
            textToApprove: null,
            openModalToDel: false,
        }
    },

    computed: {
    },
    methods: {
        getShipments: function () {
            axios.get('/shipments/', {params: {page: this.currentPage}})
                .then(response => {
                    if (response.status === 200) {
                        this.shipments = response.data.results;
                        this.currentPage = response.data.page_number;
                        this.pageCount = response.data.total_pages;
                    }
                })
                .catch(response => {
                    console.log(response);
                });
        },
        async pageChangeHandle(value) {
            switch (value) {
                case 'first':
                    this.currentPage = 1
                    break
                case 'next':
                    this.currentPage += 1
                    break
                case 'previous':
                    this.currentPage -= 1
                    break
                case 'last':
                    this.currentPage = this.pageCount
                    break
                default:
                    this.currentPage = value
            }
            this.getShipments()
            // const {data} = await axios.get(
            //     '/shipments/', {params: {page: this.currentPage}}
            // )
            // console.log(data)
            // this.articles = data.articles;
            // this.shipments = data.results;
            // this.currentPage = data.page_number;
            // this.pageCount = data.total_pages;

        },
        approveDelRecord: function (itemId) {
            this.recordToDelete = itemId;
            this.textToApprove = `Delete shipment №${itemId}?`;
            this.openModalToDel = true;
        },
        decisionToDelRecord: function (result) {
            this.openModalToDel = false;
            this.textToApprove = null;
            result ? this.deleteShipment(this.recordToDelete) : this.recordToDelete = null;
        },
        addShipment: function () {
            axios.post('/shipments/')
                .then(response => {
                    if (response.status === 204) {
                        this.getShipments()
                    }
                })
                .catch(response => {
                    console.log(response);
                });
        }
    },
    mounted() {
        this.getShipments();
    }
};
</script>
