<template>
    <v-dialog v-model="propModel" max-width="80%">
        <v-card v-if="itemDetails" class="pt-9 pb-4">
            <v-card-title v-if="!editMode" class="text-h5 ml-5">
                {{ itemDetails.title }}
            </v-card-title>

            <v-card-text>
                <v-table v-if="!editMode" density="compact">
                    <thead>
                    <tr>
                        <th class="text-left">
                            Field
                        </th>
                        <th class="text-left">
                            Value
                        </th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="(k, v) in itemDetails" :key="v">
                        <td>{{ v }}</td>
                        <td>{{ k }}</td>
                    </tr>
                    </tbody>
                </v-table>

                <formShipment v-if="editMode"
                              :item="newObject"
                              :obj-id="objId"
                              @close="editMode=false"
                              @saveChanges="updateShipment"
                />
            </v-card-text>
            <v-card-actions v-if="!editMode" class="mr-2">
                <v-spacer></v-spacer>
                <v-btn class="mr-1" color="orange-darken-3" size="small" @click="openForm">edit</v-btn>
                <v-btn class="mr-1" size="small" @click="close">close</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import axios from "axios";
import formShipment from "@/components/formShippment.vue";

export default {
    name: "dialogDetail",
    components: {
        formShipment,
    },
    props: {
        itemId: {
            type: Number,
            required: true,
        },
        dialogDetailOpen: {
            type: Boolean,
            required: true,
        },
    },
    computed: {

        propModel: {
            get() {
                return this.dialogDetailOpen
            },
        }
    },
    data: function () {
        return {
            objId: null,
            newObject: {
                title: null,
                description: null,
                status: null
            },
            itemDetails: null,
            editMode: false,
            itemWasChanged: false,
        }
    },
    methods: {
        setResult: function (result) {
            this.$emit('setResult', result)
        },
        openForm: function () {
            console.log(this.itemDetails)
            this.objId = this.itemDetails.id
            this.newObject = {
                title: this.itemDetails.title,
                description: this.itemDetails.description,
                status: this.itemDetails.status
            }
            this.editMode = true
        },
        getShipping: function () {
            axios.get('/api/shipping/' + this.itemId + '/')
                .then(response => {
                    if (response.status === 200) {
                        this.itemDetails = response.data
                    }
                })
                .catch(response => {
                    console.log(response);
                    this.close();
                });
        },
        close: function () {
            this.itemDetails = null;
            this.$emit('close', this.itemWasChanged);
        },
        updateShipment: function (result) {
            console.log(result)
            axios.patch('/api/shipping/' + this.itemDetails.id + "/", result, {
                headers: {'Content-Type': 'application/json'}
            })
                .then(response => {
                    if (response.status === 200) {
                        this.itemDetails = response.data
                        this.editMode = false
                        this.itemWasChanged = true
                    }
                })
                .catch(error => {
                    console.log(error)
                });
        }
    },
    mounted: function () {
        this.getShipping();
    },
}
</script>
