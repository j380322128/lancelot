/**
 * Created by mugbya on 2017/3/23.
 */






['8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00',
                '19:00', '20:00', '21:00', '22:00', '23:00' ]


$(function () {
    $('#chart_user').highcharts({
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
    $('#chart_user').highcharts({
        title: {
            text: '单课程趋势图',
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
    $('#chart_user').highcharts({
        title: {
            text: '课程趋势图',
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
    $('#chart_user').highcharts({
        title: {
            text: '趋势图',
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
                text: '用户数量（人）'
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
            name: '新增用户',
            data: [7, 12, 30, 35, 42, 49, 61, 68, 72, 101, 121, 220]
        }, {
            name: '新增激活用户',
            data: [4, 6, 8, 5, 20, 1, 1, 6, 16, 32, 21, 12]
        }, {
            name: '新增付费用户',
            data: [2, 4, 2, 5, 10, 2, 1, 6, 8, 3, 2, 5]
        }, {
            name: '新增活跃用户',
            data: [14, 26, 18, 1, 22, 1, 14, 6, 32, 3, 21, 22]
        }]
    });
});