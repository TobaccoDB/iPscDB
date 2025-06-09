<template>
    <div class="footer">
        <!-- <div class="footer-header">
      <div class="footer-header-left">
        <div>{{ totalviewData }}</div>
        <div>Total views</div>
      </div>
      <ul class="footer-header-right">
        <li v-for="(item, key) in viewData" :key="key">
          <div>{{ item.count }}</div>
          <div :style="item.position"></div>
        </li>
      </ul>
    </div> -->
        <!-- <div class="footer-middle"></div> -->
        <div class="footer-footer">
            <span>
                <i></i>
                <i></i>E-mail:tobaccodb@gmail.com</span
            >
        </div>
    </div>
</template>
<script>
import { cell_country_visiter } from '@/api/api'
export default {
    data() {
        return {
            totalviewData: 0,
            Correspondence: [
                {
                    country: '加拿大',
                    idx: 1
                },
                {
                    country: '澳大利亚',
                    idx: 2
                },
                {
                    country: '瑞士',
                    idx: 3
                },
                {
                    country: '中国',
                    idx: 4
                },
                {
                    country: '德国',
                    idx: 5
                },
                {
                    country: '法国',
                    idx: 6
                },
                {
                    country: '英国',
                    idx: 7
                },
                {
                    country: '美国',
                    idx: 8
                },
                {
                    country: '意大利',
                    idx: 9
                },
                {
                    country: '日本',
                    idx: 10
                },
                {
                    country: '越南',
                    idx: 11
                },
                {
                    country: '韩国',
                    idx: 12
                },
                {
                    country: '马来西亚',
                    idx: 13
                },
                {
                    country: '挪威',
                    idx: 14
                },
                {
                    country: '泰国',
                    idx: 15
                },
                {
                    country: '新加坡',
                    idx: 16
                },
                {
                    country: '孟加拉',
                    idx: 17
                },
                {
                    country: '伊朗',
                    idx: 18
                },
                {
                    country: '比利时',
                    idx: 19
                },
                {
                    country: '捷克',
                    idx: 20
                },
                {
                    country: '印度',
                    idx: 21
                },
                {
                    country: '荷兰',
                    idx: 22
                }
            ],
            viewData: []
        }
    },
    mounted() {
        // this.post_detail();
    },
    methods: {
        post_detail() {
            cell_country_visiter({}).then((res) => {
                this.totalviewData = res.total_count
                res.data.forEach((item, index) => {
                    this.Correspondence.forEach((items) => {
                        if (item.country === items.country) {
                            item.position = `background-position: 0 -${Number(items.idx) * 32}px;`
                        }
                    })
                })
                this.viewData = res.data
            })
        }
    }
}
</script>
<style lang="scss" scoped>
.footer {
    width: 100%;
    height: 70px;
    background: #f4f4f4;
    position: fixed;
    left: 0;
    bottom: 0;
    z-index: 999999;

    .footer-footer {
        // height: 73px;
        // line-height: 73px;
        height: 70px;
        line-height: 70px;
        float: left;
        width: 100%;
        text-align: center;
        font-size: 18px;
        font-family: PingFang SC;
        font-weight: 500;
        color: rgba(51, 51, 51, 1);
        background: #b2dbc6;
        i {
            display: inline-block;
            width: 60px;
            height: 40px;
            position: absolute;
            top: 15px;
            // top: 12px;
            left: 0;
        }
        span i:first-child {
            background: url(~@/assets/img/footerIcon1.png) no-repeat 100%;
            background-size: contain;
        }
        span i:nth-child(2) {
            background: url(~@/assets/img/footerIcon2.png) no-repeat 100%;
            background-size: contain;
            left: 74px;
        }
        span {
            display: inline-block;
            position: relative;
            padding-left: 150px;
        }
    }
}
.footer .footer-header {
    float: left;
    width: 100%;
    height: 87px;
    display: flex;
    justify-content: center;
}
.footer .footer-header .footer-header-left {
    margin: 0;
    padding: 0;
    float: left;
    width: 120px;
    overflow: hidden;
}
.footer .footer-header .footer-header-left div:first-child {
    margin-top: 20px;
    width: 100%;
    height: 22px;
    font-size: 24px;
    font-family: PingFang SC;
    font-weight: 500;
    color: #333;
    line-height: 22px;
    text-align: center;
}

.footer .footer-header .footer-header-left div:last-child {
    margin-top: 15px;
    width: 100%;
    height: 16px;
    font-size: 20px;
    font-family: PingFang SC;
    font-weight: 400;
    color: #666;
    line-height: 16px;
    text-align: center;
}
.footer .footer-header .footer-header-right {
    list-style: none;
    margin: 0;
    padding: 0;
    float: left;
    width: 1120px;
    height: 87px;
    overflow: hidden;
}
.footer .footer-header .footer-header-right li {
    margin: 0;
    float: left;
    width: 12.5%;
    height: 100%;
}

.footer .footer-header .footer-header-right li div:first-child {
    margin-top: 23px;
    width: 100%;
    font-size: 20px;
    font-family: PingFang SC;
    font-weight: 400;
    color: #333;
    line-height: 16px;
    height: 16px;
    text-align: center;
}

.footer .footer-header .footer-header-right li div:last-child {
    margin: 0 auto;
    margin-top: 10px;
    height: 28px;
    width: 30px;
    background: url(../../assets/img/flags_test.png) no-repeat;
}

.footer .footer-middle {
    width: 100%;
    height: 1px;
    margin: 0 auto;
    background: rgba(225, 228, 230, 1);
}
</style>
