/**
 * Created by mugbya on 16-10-8.
 */


$(function () {
    $('#city').highcharts({
        chart: {
            type: 'bar'
        },

        // chart: {
        //     plotBackgroundColor: null,
        //     plotBorderWidth: null,
        //     plotShadow: false
        // },

        title: {
            text: '城市分布图'
        },
        subtitle: {
            text: '数据来源: 有获网络'
        },
        xAxis: {
            categories: ['上海', '北京', '杭州 ', '广州', '其他'],
            title: {
                text: null
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: '人数 (人)',
                align: 'high'
            },
            labels: {
                overflow: 'justify'
            }
        },
        tooltip: {
            valueSuffix: ' 人'
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                }
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -40,
            y: 100,
            floating: true,
            borderWidth: 1,
            backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
            shadow: true
        },
        credits: {
            enabled: false
        },
        series: [{
            data: [3012, 2748, 1635, 1203, 1067]
        }]
        // tooltip: {
        //     headerFormat: '{series.name}<br>',
        //     pointFormat: '{point.name}: <b>{point.percentage:.1f}%</b>'
        // },
        // plotOptions: {
        //     pie: {
        //         allowPointSelect: true,
        //         cursor: 'pointer',
        //         dataLabels: {
        //             enabled: false
        //         },
        //         showInLegend: true
        //     }
        // },
        // series: [{
        //     type: 'pie',
        //     name: '浏览器访问量占比',
        //     data: [
        //         ['上海',   45.0],
        //         ['北京',       26.8],
        //         {
        //             name: '杭州',
        //             y: 12.8,
        //             sliced: true,
        //             selected: true
        //         },
        //         ['深圳',    14.7],
        //         ['其他',   0.7]
        //     ]
        // }]
    });
});

$(function () {
    $('#all_course').highcharts({
        title: {
            text: '趋势图',
            x: -20 //center
        },
        subtitle: {
            text: '来源：有获网络',
            x: -20
        },
        xAxis: {
            categories: ['2017-03-05', '2017-03-06','2017-03-07', '2017-03-08', '2017-03-09', '2017-03-10',
                '2017-03-11', '2017-03-12', '2017-03-13', '2017-03-14', '2017-03-15', '2017-03-16', '2017-03-17',
                '2017-03-18', '2017-03-19', '2017-03-20']
        },
        yAxis: {
            title: {
                text: '用户数量（人）| 次数 (次)'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: '人'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: '课程访问次数',
            data: [147, 179, 146, 235, 242, 249, 181, 168, 172, 201, 221, 220]
        }, {
            name: '报名人数',
            data: [84, 86, 88, 85, 80, 81, 81, 86, 86, 82, 81, 82]
        }, {
            name: '观看人数',
            data: [84, 86, 88, 85, 78, 81, 81, 86, 86, 82, 79, 82]
        }, {
            name: '分享次数',
            data: [114, 126, 118, 111, 122, 111, 114, 116, 132, 113, 121, 122]
        }]
    });
});


$(function () {
    $('#course').highcharts({
        title: {
            text: '趋势图',
            x: -20 //center
        },
        subtitle: {
            text: '来源：有获网络',
            x: -20
        },
        xAxis: {
            categories: ['2017-03-05', '2017-03-06','2017-03-07', '2017-03-08', '2017-03-09', '2017-03-10',
                '2017-03-11', '2017-03-12', '2017-03-13', '2017-03-14', '2017-03-15', '2017-03-16', '2017-03-17',
                '2017-03-18', '2017-03-19', '2017-03-20']
        },
        yAxis: {
            title: {
                text: '用户数量（人）| 次数 (次)'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: '人'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: '课程访问次数',
            data: [68, 79, 66, 75, 82, 79, 81, 63, 72, 91, 88, 83]
        }, {
            name: '报名人数',
            data: [46, 45, 54, 49, 50, 51, 48, 56, 58, 48, 53, 48]
        }, {
            name: '观看人数',
            data: [46, 45, 52, 49, 50, 49, 48, 56, 58, 48, 51, 46]
        }, {
            name: '分享次数',
            data: [22, 26, 28, 21, 29, 22, 24, 26, 22, 33, 21, 22]
        }]
    });
});


$(function () {
    $('#phone').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            text: '终端分布图'
        },
        tooltip: {
            headerFormat: '{series.name}<br>',
            pointFormat: '{point.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false
                },
                showInLegend: true
            }
        },
        series: [{
            type: 'pie',
            name: '终端 访问量占比',
            data: [
                ['iPhone6s',   45.0],
                ['小米',       26.8],
                {
                    name: 'Mate9',
                    y: 12.8,
                    sliced: true,
                    selected: true
                },
                ['荣耀8',    8.5],
                ['iPad',     6.2],
                ['其他',   0.7]
            ]
        }]
    });
});


$(function () {
    $('#course_user').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: '课程参与度分布'
        },
        subtitle: {
            text: '数据截止 2017-03-20，来源: 有获网络'
        },
        xAxis: {
            type: 'category',
            labels: {
                rotation: -45,
                style: {
                    fontSize: '15px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: '参与人数 (人)'
            }
        },
        legend: {
            enabled: false
        },
        tooltip: {
            pointFormat: '参与数: <b>{point.y} 人</b>'
        },
        series: [{
            name: '总人数',
            data: [
                ['10', 244],
                ['20', 233],
                ['30', 178],
                ['40', 204],
                ['50', 244],
                ['60', 186],
                ['70', 198],
                ['80', 214],
                ['90', 184],
                ['100', 182],

            ],
            dataLabels: {
                enabled: true,
                rotation: -90,
                color: '#FFFFFF',
                align: 'right',
                y: 10, // 10 pixels down from the top
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        }]
    });
});


$(function () {
    $('#course_jack').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: '课程指标概览'
        },
        subtitle: {
            text: '数据来源: 有获网络'
        },
        xAxis: {
            categories: [
                '樊登读书会',
                '中国商业趋势和未来解读',
                '企业成长中的变革管理'
            ],
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: '人数 | 次数'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: '课程访问次数',
            data: [322, 396, 376]
        }, {
            name: '报名人数',
            data: [303, 395, 376]
        }, {
            name: '观看人数',
            data: [302, 395, 376]
        }, {
            name: '分享次数',
            data: [198, 214, 297]
        }]
    });
});





$(function () {
    $('#chart_star').highcharts({
        title: {
            text: '关于大咖增长率曲线',
            x: -20 //center
        },
        subtitle: {
            text: '来源：有获网络',
            x: -20
        },
        xAxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        },
        yAxis: {
            title: {
                text: '大咖数量（人）'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: '人'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: '新增大咖',
            data: [7, 12, 30, 35, 42, 49, 61, 68, 72, 101, 121, 220]
        }, {
            name: '新增激活大咖',
            data: [4, 6, 8, 5, 20, 1, 1, 6, 16, 32, 21, 12]
        }]
    });
});
$(function () {
    $('#chart_livePlaying').highcharts({
        title: {
            text: '关于直播增长率曲线',
            x: -20 //center
        },
        subtitle: {
            text: '来源：有获网络',
            x: -20
        },
        xAxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        },
        yAxis: {
            title: {
                text: '直播数量（个）'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: '个'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: '直播数',
            data: [7, 12, 30, 35, 42, 49, 61, 68, 72, 101, 121, 220]
        }, {
            name: '平均付费购买数',
            data: [4, 6, 8, 5, 20, 1, 1, 6, 16, 32, 21, 12]
        }, {
            name: '平均有帮助数',
            data: [4, 6, 8, 5, 20, 1, 1, 6, 16, 32, 21, 12]
        }, {
            name: '平均没有帮助数',
            data: [4, 6, 8, 5, 20, 1, 1, 6, 16, 32, 21, 12]
        }, {
            name: '平均评论数',
            data: [4, 6, 8, 5, 20, 1, 1, 6, 16, 32, 21, 12]
        }]
    });
});
$(function () {
    $('#chart_recorded').highcharts({
        title: {
            text: '关于录播增长率曲线',
            x: -20 //center
        },
        subtitle: {
            text: '来源：有获网络',
            x: -20
        },
        xAxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        },
        yAxis: {
            title: {
                text: '录播数量（个）'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: '个'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: '录播课程数',
            data: [7, 12, 30, 35, 42, 49, 61, 68, 72, 101, 121, 220]
        }, {
            name: '平均付费购买数',
            data: [4, 6, 8, 5, 20, 1, 1, 6, 16, 32, 21, 12]
        }, {
            name: '平均有帮助数',
            data: [4, 6, 8, 5, 20, 1, 1, 6, 16, 32, 21, 12]
        }, {
            name: '平均没有帮助数',
            data: [4, 6, 8, 5, 20, 1, 1, 6, 16, 32, 21, 12]
        }, {
            name: '平均评论数',
            data: [4, 6, 8, 5, 20, 1, 1, 6, 16, 32, 21, 12]
        }]
    });
});
$(function () {
    $('#chart_column').highcharts({
        title: {
            text: '关于专栏增长率曲线',
            x: -20 //center
        },
        subtitle: {
            text: '来源：有获网络',
            x: -20
        },
        xAxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        },
        yAxis: {
            title: {
                text: '专栏数量（个）'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: '个'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: '专栏文章数',
            data: [7, 12, 30, 35, 42, 49, 61, 68, 72, 101, 121, 220]
        }, {
            name: '平均付费购买数',
            data: [4, 6, 8, 5, 20, 1, 1, 6, 16, 32, 21, 12]
        }, {
            name: '平均有帮助数',
            data: [4, 6, 8, 5, 20, 1, 1, 6, 16, 32, 21, 12]
        }, {
            name: '平均没有帮助数',
            data: [4, 6, 8, 5, 20, 1, 1, 6, 16, 32, 21, 12]
        }, {
            name: '平均平均数',
            data: [4, 6, 8, 5, 20, 1, 1, 6, 16, 32, 21, 12]
        }]
    });
});
$(function () {
    $('#chart_QA').highcharts({
        title: {
            text: '关于问答增长率曲线',
            x: -20 //center
        },
        subtitle: {
            text: '来源：有获网络',
            x: -20
        },
        xAxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        },
        yAxis: {
            title: {
                text: '问答数量（个）'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: '个'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: '新增问题',
            data: [7, 12, 30, 35, 42, 49, 61, 68, 72, 101, 121, 220]
        }, {
            name: '新增答案',
            data: [4, 6, 8, 5, 20, 1, 1, 6, 16, 32, 21, 12]
        }, {
            name: '平均问题答案数',
            data: [4, 6, 8, 5, 20, 1, 1, 6, 16, 32, 21, 12]
        }, {
            name: '付费购买数',
            data: [4, 6, 8, 5, 20, 1, 1, 6, 16, 32, 21, 12]
        }]
    });
});