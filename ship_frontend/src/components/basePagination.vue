<template>
    <div >
                <v-btn icon="mdi-account" size="x-small" class="mr-1"
                :disabled="isPreviousButtonDisabled"
                @click="firstPage"
        >
            ←←
        </v-btn>
        <v-btn icon="mdi-account" size="x-small" class="mr-1"
                :disabled="isPreviousButtonDisabled"
                @click="previousPage"
        >
            ←
        </v-btn>
        <BasePaginationItem
                v-for="paginationTrigger in paginationTriggers"
                :key="paginationTrigger"
                :pageNumber="paginationTrigger"
                :current-page="currentPage"
                class="base-pagination__description"
                @loadPage="onLoadPage"
        />
        <v-btn icon="mdi-account" size="x-small" class="mr-1"
                :disabled="isNextButtonDisabled"
                @click="nextPage"
        >
            →
        </v-btn>
        <v-btn icon="mdi-account" size="x-small" class="mr-1"
                :disabled="isNextButtonDisabled"
                @click="lastPage"
        >
            →→
        </v-btn>

    </div>
</template>
<script>
import BasePaginationItem from "./basePaginationItem.vue";

export default {
    components: {
        BasePaginationItem
    },
    props: {
        visiblePagesCount: {
            type: Number,
            required: true
        },
        currentPage: {
            type: Number,
            required: true
        },
        pageCount: {
            type: Number,
            required: true
        }
    },
    computed: {
        isPreviousButtonDisabled() {
            return this.currentPage === 1
        },
        isNextButtonDisabled() {
            return this.currentPage === this.pageCount
        },
        paginationTriggers() {
            const currentPage = this.currentPage
            const pageCount = this.pageCount
            const visiblePagesCount = this.visiblePagesCount

            let pagintationTriggersArray = Array.from({ length: this.pageCount }, (_, i) => i + 1)
            if (this.pageCount <= visiblePagesCount) {
                return pagintationTriggersArray
            }

            const visiblePagesThreshold = (visiblePagesCount - 1) / 2
            pagintationTriggersArray = Array(this.visiblePagesCount - 1).fill(0)

            if (currentPage <= visiblePagesThreshold + 1) {
                pagintationTriggersArray[0] = 1
                const pagintationTriggers = pagintationTriggersArray.map(
                    (paginationTrigger, index) => {
                        return pagintationTriggersArray[0] + index
                    }
                )
                return pagintationTriggers
            }
            if (currentPage >= pageCount - visiblePagesThreshold + 1) {
                const pagintationTriggers = pagintationTriggersArray.map(
                    (paginationTrigger, index) => {
                        return pageCount - index
                    }
                )
                pagintationTriggers.reverse()
                return pagintationTriggers
            }
            pagintationTriggersArray[0] = currentPage - visiblePagesThreshold + 1
            const pagintationTriggers = pagintationTriggersArray.map(
                (paginationTrigger, index) => {
                    return pagintationTriggersArray[0] + index
                }
            )
            return pagintationTriggers
        },},
    methods: {
        firstPage() {
            this.$emit('firstPage');
        },
        nextPage() {
            this.$emit('nextPage');
        },
        lastPage() {
            this.$emit('lastPage');
        },
        previousPage() {
            this.$emit('previousPage');
        },
        onLoadPage(value) {
            this.$emit("loadPage", value);
        }
    }
}
</script>