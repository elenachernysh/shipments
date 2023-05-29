<template>
    <v-dialog v-model="propModel" max-width="450">
        <v-card class="pt-9 pb-4">
            <v-card-text>{{ text }}</v-card-text>
            <v-card-actions class="mr-2">
                <v-spacer></v-spacer>
                <v-btn size="small" class="mr-1 elevated" color="orange-darken-3" @click="setResult(true)">
                    yes
                </v-btn>
                <v-btn size="small" class="mr-1" @click="setResult(false)">
                    no
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
export default {
    name: "dialogModal",
    props: {
        dialogModalOpen: {
            type: Boolean,
            required: true,
        },
        text: {
            type: String,
            required: true,
        }
    },
    computed: {
        propModel: {
            get() {
                return this.dialogModalOpen
            },
        }
    },
    data: function () {
        return {}
    },
    methods: {
        setResult: function (result) {
            this.$emit('setResult', result)
        },
    }
}
</script>
