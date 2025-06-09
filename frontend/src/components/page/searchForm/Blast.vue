<template>
    <div class="Blast">
        <div class="marker-header">
            <el-breadcrumb separator-class="el-icon-arrow-right">
                <el-breadcrumb-item :to="{ path: '/searchForm' }">Search</el-breadcrumb-item>
                <el-breadcrumb-item>Search result</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="Blast-content">
            <div class="BlastName">
                <h1>Blast Results</h1>
            </div>
            <el-table :data="tableData" style="width: 100%">
                <el-table-column prop="label" label="Gene ID" align="center"> </el-table-column>
                <el-table-column prop="name" label="Species" align="center"> </el-table-column>
                <el-table-column prop="label" label="Gene Symbol" align="center"> </el-table-column>
                <el-table-column prop="name" label="Description" align="center"> </el-table-column>
            </el-table>
            <div class="TableItemBody">
                <el-pagination
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="queryInfo.page"
                    :page-sizes="[10, 20, 30, 50]"
                    :page-size="queryInfo.page_size"
                    layout="total, sizes, prev, pager, next"
                    :total="count"
                    background
                >
                </el-pagination>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            tableData: [
                { label: 'CD14', name: 100 },
                { label: 'CD14', name: 100 },
                { label: 'CD14', name: 100 },
                { label: 'CD14', name: 100 },
                { label: 'CD14', name: 100 },
                { label: 'CD14', name: 100 },
                { label: 'CD14', name: 100 },
                { label: 'CD14', name: 100 },
                { label: 'CD14', name: 100 },
                { label: 'CD14', name: 100 }
            ],
            queryInfo: {
                page: 1,
                page_size: 10
            },
            count: 100
        }
    },
    methods: {
        handleSizeChange() {},
        handleCurrentChange() {}
    }
}
</script>

<style scoped lang="scss">
.Blast {
    width: 1240px;
    height: auto;
    margin: 0 auto;
    .marker-header {
        width: 100%;
        height: 40px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
    }
    .Blast-content {
        background: #fff;
        padding: 20px;
        box-sizing: border-box;
    }
    .BlastName {
        width: 100%;
        height: 50px;
        border-bottom: 1px solid #ccc;
    }
    .TableItemBody {
        height: 50px;
        width: 100%;
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }
}
</style>

<style lang="scss">
.TableItemBody {
    .el-pagination.is-background .el-pager li:not(.disabled).active {
        background-color: #24a461 !important;
    }
    .el-radio__input.is-checked + .el-radio__label {
        color: #24a461 !important;
    }
    .el-radio__input.is-checked .el-radio__inner {
        background: #24a461 !important;
        color: #24a461 !important;
        border-color: #24a461 !important;
    }
    .el-button--primary {
        background: #24a461 !important;
        border-color: #24a461 !important;
        font-size: 16px;
    }
}
</style>
