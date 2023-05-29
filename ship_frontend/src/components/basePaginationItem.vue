<template>
    <v-btn icon="mdi-account" size="x-small" class="mr-1" @click="onClick" :disabled="isDisabled" :color="isDisabled ? 'orange-darken-3' : ''">
        {{ pageNumber }}
    </v-btn>
</template>
<script>
export default {
    props: {
        pageNumber: {
            type: Number,
            required: true
        },
        currentPage: {
            type: Number,
            required: true
        }
    },
    computed: {
        isDisabled() {
            return this.pageNumber === this.currentPage
        },
    },
    methods: {
        onClick() {
            this.$emit("loadPage", this.pageNumber)
        }
    }
}
</script>
