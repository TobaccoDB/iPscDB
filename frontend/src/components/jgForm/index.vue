<template>
  <div class="jg-form" v-bind:class="{ smallForm: isSmallForm }">
    <div class="title" v-if="title">{{title}}</div>
    <el-form ref="searchForm" :inline="isInline" :model="formData" :rules="rules" :label-position="labelPosition">
      <slot></slot>
      <el-form-item class="form-item" :label-width="labelWidth" :label="item.label" :prop="item.key" v-for="(item, index) in formConfig"
        :key="index">
        <!-- input -->
        <el-input :size="inputSize" v-if="item.type === 'input'" v-model="formData[item.key]" :placeholder="item.placeholder" :disabled="item.disabled"
          v-bind:style="{ width: item.width? item.width: inputWidth, margin:item.margin }" @keyup.enter.native="handleSearch()"></el-input>
        <!-- inputArea -->
        <el-input :size="inputSize" v-if="item.type === 'inputArea'" v-model="formData[item.key1]" :placeholder="item.placeholder"
          :disabled="item.disabled" v-bind:style="{ width: item.width? item.width: inputWidth }"></el-input>
        <span v-if="item.type === 'inputArea'"> - </span>
        <el-input :size="inputSize" v-if="item.type === 'inputArea'" v-model="formData[item.key2]" :placeholder="item.placeholder"
          :disabled="item.disabled" v-bind:style="{ width: item.width? item.width: inputWidth }"></el-input>
        <!-- textarea -->
        <el-input v-if="item.type === 'textarea'" :type="item.type" v-model="formData[item.key]" :placeholder="item.placeholder"
          :disabled="item.disabled" :rows="item.rows" v-bind:style="{ width: item.width ? item.width : inputWidth }"></el-input>
        <!-- select -->
        <el-select :size="inputSize" v-if="item.type === 'select'" :multiple="item.isMultiple" v-model="formData[item.key]" :placeholder="item.placeholder"
          :filterable="item.isFilterable" :disabled="item.disabled" :clearable="item.clearable" @change="handleSelect(index)"
          v-bind:style="{ width: item.width? item.width: inputWidth, margin:item.margin }">
          <el-option v-for="option in item.options" :key="option.value" :value="option.value" :label="option.text">
          </el-option>
        </el-select>
        <!-- date-picker -->
        <el-date-picker :size="inputSize" v-bind:style="{ width: item.width? item.width: inputWidth }" v-if="item.type === 'datePicker'"
          v-model="formData[item.key]" :unlink-panels="item.dateType === 'daterange'" :type="item.dateType" :value-format="item.valueFormat"
          :range-separator="item.rangeSeparator" :start-placeholder="item.startText" :end-placeholder="item.endText" :placeholder="item.placeholder"
          @change="dateChange">
        </el-date-picker>
      </el-form-item>
      <el-form-item class="form-btn" v-if="hasReset || hasSearch || hasIconSearch || hasSecondSearch">
        <el-button :size="inputSize" v-if="hasIconSearch" type="primary" @click="handleSearch" class="search" icon="el-icon-search"></el-button>
        <el-button :size="inputSize" v-if="hasSearch" type="primary" @click="handleSearch" class="search">{{firstBtnText}}</el-button>
        <el-button :size="inputSize" v-if="hasSecondSearch" type="primary" @click="handleSecondSearch" class="search">{{secondBtnText}}</el-button>
        <el-button :size="inputSize" v-if="hasReset" type="primary" @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'jg-form',
  props: {
    title: {
      type: String,
      default() {
        return ''
      }
    },
    formData: {
      type: Object,
      default() {
        return {}
      }
    },
    formConfig: {
      type: Array,
      default() {
        return []
      }
    },
    hasIconSearch: {
      type: Boolean,
      default() {
        return false
      }
    },
    hasSearch: {
      type: Boolean,
      default() {
        return true
      }
    },
    hasSecondSearch: {
      type: Boolean,
      default() {
        return false
      }
    },
    hasReset: {
      type: Boolean,
      default() {
        return true
      }
    },
    isInline: {
      type: Boolean,
      default() {
        return true
      }
    },
    labelWidth: {
      type: String,
      default() {
        return 'auto'
      }
    },
    labelPosition: {
      type: String,
      default() {
        return 'left'
      }
    },
    rules: {
      type: Object,
      default() {
        return {}
      }
    },
    checkFormStatu: {
      type: String,
      default() {
        return ''
      }
    },
    inputWidth: {
      type: String,
      default() {
        return 'auto'
      }
    },
    inputSize: {
      type: String,
      default() {
        return 'middle'
      }
    },
    isSmallForm: {
      type: Boolean,
      default() {
        return false
      }
    },
    firstBtnText: {
      type: String,
      default() {
        return '搜索'
      }
    },
    secondBtnText: {
      type: String,
      default() {
        return '搜索'
      }
    }
  },
  data() {
    return {
      isLineFeed: {
        width: '100%',
        display: 'block'
      }
    }
  },
  methods: {
    handleReset() {
      this.$emit('handleReset')
    },
    handleSearch() {
      this.$emit('handleSearch')
    },
    handleSecondSearch() {
      this.$emit('handleSecondSearch')
    },
    handleSelect(index) {
      this.$emit('handleSelect', index)
    },
    checkForm() {
      let validValue = true
      this.$refs['searchForm'].validate((valid) => {
        if (valid) {
          validValue = true
        } else {
          validValue = false
        }
      })
      return validValue
    },
    resetForm() {
      this.$refs['searchForm'].resetFields()
    },
    dateChange(val) {
      this.$emit('dateChange', val)
    }
  },
  watch: {
    checkFormStatu(val) {
      switch (val) {
        case 'checking':
          this.$emit('checkForm', this.checkForm())
          break
        case 'reset':
          this.resetForm()
          break
      }
    }
  }
}
</script>

<style scoped>
@import "./style.css";
</style>
