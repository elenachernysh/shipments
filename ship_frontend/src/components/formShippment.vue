<template>
    <div>
    <div class="text-h5 mb-5">
        <span v-if="objId">Edit</span>
        <span v-else>Create</span>
    </div>

    <v-form @submit.prevent="save" ref="shipForm">
        <v-text-field
                v-model="item.title"
                :rules="titleRules"
                label="title"
                required
        ></v-text-field>
        <v-text-field
                v-model="item.description"
                :rules="descriptionRules"
                label="description"
                required
        ></v-text-field>
        <v-select
                v-model="item.status"
                :items="statusValues"
                :rules="[v => !!v || 'Status is required']"
                label="Status"
                required
        ></v-select>

        <v-btn size="small" class="mr-1" color="orange-darken-3" @click.prevent="save">save</v-btn>
        <v-btn size="small" class="mr-1" @click="$emit('close')">close</v-btn>
    </v-form>
    </div>
</template>

<script>
export default {
    name: "formShipment",
    props: {
        objId: {
            type: Number,
            required: false,
        },
        item: {
            type: Object,
            required: true,
        },
    },
    computed: {},
    data: () => ({
        statusValues: [
            'draft', 'published', 'staged', 'done', 'declined'
        ],
        titleRules: [
            v => !!v || 'Field is required',
            v => (v && v.length < 50) || 'Title must be less than 50 characters',
        ],
        descriptionRules: [
            v => !!v || 'Field is required',
            v => (v && v.length < 150) || 'Description must be less than 150 characters',
        ],
    }),
    methods: {
        save: function () {
            let result = {
                "title": this.item.title,
                "description": this.item.description,
                "status": this.item.status
            }
            this.$emit('saveChanges', result);
        },
    }
}
</script>