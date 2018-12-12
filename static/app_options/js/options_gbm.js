// 绘制直方图
var chart1 = null;

$(document).ready(function() {
    chart1 = Highcharts.chart('container_1', {
    chart1: {
        events: {
            load: api_get_gbm_data // 图表加载完毕后执行的回调函数
        }
    },
    title: {
        text: ''
    },
    xAxis: [{
        title: { text: '数据点' }
        }, {
        title: { text: '价格' },
        opposite: true
    }],
    yAxis: [{
        title: { text: '价格' }
        }, {
        title: { text: '分布数量' },
        opposite: true
    }],
    series: [{
        name: '直方图',
        type: 'histogram',
        xAxis: 1,
        yAxis: 1,
        baseSeries: 's1',
        zIndex: -1
        }, {
        name: '数据点',
        type: 'scatter',
        data: [1,2,3,4,5,6,6,7,9],
        id: 's1',
        marker: {
            radius: 0.8
        }}
    ],
    credits:{enabled:false}
    });
})


// post表单，从API获取gbm模拟data
function api_get_gbm_data() {
    var pricing_date_y = $('#pricing_date_y').val();
    var pricing_date_m = $('#pricing_date_m').val();
    var pricing_date_d = $('#pricing_date_d').val();

    var final_date_y = $('#final_date_y').val();
    var final_date_m = $('#final_date_m').val();
    var final_date_d = $('#final_date_d').val();

    var initial_value = $('#initial_value').val();
    var volatility = $('#volatility').val();
    var frequency = $('#frequency').val();
    var csr = $('#csr').val();
    var paths = $('#paths').val();

    var currency = $('#currency').val();

    $.ajax({
        type : 'post',
        url: '/options/gbm_json/',
        data: {
            pricing_date_y: pricing_date_y,
            pricing_date_m: pricing_date_m,
            pricing_date_d: pricing_date_d,
            final_date_y: final_date_y,
            final_date_m: final_date_m,
            final_date_d: final_date_d,
            initial_value: initial_value,
            volatility: volatility,
            frequency: frequency,
            csr: csr,
            paths: paths,
            currency: currency,
        },
        dataType : 'json',
        success: function(ret) {
             chart1.series[1].setData(ret.data);
            // console.log(chart.series[1].data)
        },
        cache: false
    });
}


// 从API获取gbm模拟的一条路径

function api_get_gbm_data_path() {
    $.ajax({
        url: '/options/gbm_json_path_data/',
        dataType : 'json',
        success: function(ret) {
            console.log(ret.path_list)
            chart2.series[0].setData(ret.path_list)
            chart2.xAxis[0].update({categories: ret.time_list})

        },
        cache: false
    });
}


var chart2= Highcharts.chart('container_2', {
	chart2: {
		type: 'spline',
        events: {
            load: api_get_gbm_data_path // 图表加载完毕后执行的回调函数
        },
	},
	title: {
		text: ''
	},
	xAxis: {
		categories: [1,2,3,]
	},
	yAxis: {
		title: {
			text: '价格'
		},
	},
	tooltip: {
		crosshairs: true,
		shared: true
	},
	plotOptions: {
		spline: {
			marker: {
				radius: 4,
				lineColor: '#666666',
				lineWidth: 1
			}
		}
	},
	series: [{
		name: '标的资产价格',
		marker: {
			symbol: 'circle'
		},
		data: [4,5,6,9]
	}, ],
    credits:{enabled:false},
});