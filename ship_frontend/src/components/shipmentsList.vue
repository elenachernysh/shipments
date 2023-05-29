<template>
    <div id="shipment">
        <v-app-bar app color="orange-darken-3" dark dense>
            <v-app-bar-title>
                Shipping items
            </v-app-bar-title>

            <logout/>
        </v-app-bar>
        <v-main>

            <v-container v-if="shipments" class="mt-5 pa-5 bg-grey-lighten-3">
                <v-btn v-if="!openCreateForm"
                       class="mr-1" color="orange-darken-3" size="small"
                       @click="openCreate"
                >
                    add new shipping
                </v-btn>

                <formShipment v-if="openCreateForm"
                              :item="newObject"
                              @close="openCreateForm=false"
                              @saveChanges="createShipment"
                />

                <v-divider class="my-5"></v-divider>

                <div v-if="shipments.length">
                    <v-table class="pa-5 h-auto w-screen" density="compact">
                        <thead>
                        <tr>
                            <th v-for="k in Object.keys(shipments[0])" class="text-left">
                                {{ k }}
                            </th>
                            <th class="text-left">actions</th>
                        </tr>
                        </thead>

                        <tbody>
                        <tr v-for="item in shipments"
                            :key="item.name"
                        >
                            <td v-for="v in Object.values(item)">
                                {{ v }}
                            </td>
                            <td>
                                <v-btn class="mr-1" size="x-small" @click="openDetailView(item.id)">
                                    details
                                </v-btn>
                                <v-btn class="mr-1" size="x-small" @click="approveDelRecord(item.id)">
                                    delete
                                </v-btn>

                            </td>
                        </tr>
                        </tbody>
                    </v-table>

                    <div class="d-flex flex-row-reverse">
                        <basePagination
                                :current-page="currentPage"
                                :page-count="pageCount"
                                :visible-pages-count="pageVisibleCount"
                                class="pt-5"
                                @firstPage="pageChangeHandle('first')"
                                @lastPage="pageChangeHandle('last')"
                                @loadPage="pageChangeHandle"
                                @nextPage="pageChangeHandle('next')"
                                @previousPage="pageChangeHandle('previous')"
                        />
                    </div>
                </div>

                <dialogModal v-if="openModalToDel"
                             :dialogModalOpen="openModalToDel"
                             :text="textToApprove"
                             @setResult="decisionToDelRecord">
                </dialogModal>

                <dialogDetail v-if="openDetails"
                              :dialogDetailOpen="openDetails"
                              :item="itemDetails"
                              :itemId="currentItemId"
                              @close="closeDetails"
                              @setResult="">
                </dialogDetail>
            </v-container>
        </v-main>
    </div>
</template>

<script>
import axios from "@/axiosAPI.js";
import basePagination from "@/components/basePagination.vue";
import dialogModal from "@/components/dialogModal.vue";
import dialogDetail from "@/components//dialogDetail.vue";
import formShipment from "@/components/formShippment.vue";
import logout from "@/components/logout.vue";

export default {
    name: "shipment",
    components: {
        formShipment,
        basePagination,
        dialogModal,
        dialogDetail,
        logout,
    },

    data() {
        return {
            shipments: null,
            currentPage: 1,
            pageSize: 10,
            pageVisibleCount: 5,
            pageCount: 0,
            modalDelRecord: false,
            textToApprove: null,
            openModalToDel: false,
            itemDetails: null,
            openDetails: false,
            currentItemId: null,
            openCreateForm: false,
            newObject: {
                title: null,
                description: null,
                status: null
            },
        }
    },
    methods: {
        openCreate: function () {
            this.openCreateForm = true;
            this.newObject = {
                title: null,
                description: null,
                status: null
            };
        },
        getShipments: function () {
            axios.get('/api/shipping/', {
                params: {page: this.currentPage}
            })
                .then(response => {
                    if (response.status === 200) {
                        this.shipments = response.data.results
                        this.currentPage = response.data.page_number
                        this.pageCount = response.data.total_pages
                    }
                })
                .catch(response => {
                    console.log(response)
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
            this.getShipments();
        },
        approveDelRecord: function (itemId) {
            this.recordToDelete = itemId
            this.textToApprove = `Delete shipment №${itemId}?`
            this.openModalToDel = true
        },
        decisionToDelRecord: function (result) {
            this.openModalToDel = false
            this.textToApprove = null
            result ? this.deleteShipment(this.recordToDelete) : this.recordToDelete = null
        },
        deleteShipment: function () {
            axios.delete('/api/shipping/' + this.recordToDelete)
                .then(response => {
                    if (response.status === 204) {
                        if (this.currentPage === this.pageCount) this.currentPage = 1;
                        this.getShipments();
                    }
                })
                .catch(response => {
                    console.log(response)
                });
        },
        openDetailView: function (itemId) {
            this.openDetails = true
            this.currentItemId = itemId
        },
        closeDetails: function (itemWasChanged) {
            this.openDetails = false
            if (itemWasChanged) {
                this.getShipments()
            }
        },
        createShipment: function (result) {
            axios.post('/api/shipping/', result, {
                headers: {'Content-Type': 'application/json'}
            })
                .then(response => {
                    if (response.status === 201) {
                        this.itemDetails = response.data
                        this.openCreateForm = false
                        this.getShipments()
                    }
                })
                .catch(error => {
                    console.log(error);
                    this.openCreateForm = false;
                });
        }
    },
    mounted() {
        this.getShipments()
    }
};
</script>

