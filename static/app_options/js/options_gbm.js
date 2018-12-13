// ******************************************************************************************************
// 绘制直方图
var chart1 = null;

$(document).ready(function() {
    chart1 = Highcharts.chart('container_1', {
    chart1: {
        events: {
            load: api_gbm_data // 图表加载完毕后执行的回调函数
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
            radius: 0.5
        }}
    ],
    credits:{enabled:false}
    });
})

// post表单，从API获取gbm模拟data
var random_path = [];
var call_all_options_values = [];
var call_options_value = 0.0;
var put_all_options_values = [];
var put_options_value = 0.0;
var s_list,call_p_list,call_d_list,call_v_list,put_p_list,put_d_list,put_v_list = []

function api_gbm_data() {
    var pricing_date_y = $('#pricing_date_y').val();
    var pricing_date_m = $('#pricing_date_m').val();
    var pricing_date_d = $('#pricing_date_d').val();

    var maturity_date_y = $('#maturity_date_y').val();
    var maturity_date_m = $('#maturity_date_m').val();
    var maturity_date_d = $('#maturity_date_d').val();

    var final_date_y = $('#final_date_y').val();
    var final_date_m = $('#final_date_m').val();
    var final_date_d = $('#final_date_d').val();

    var initial_value = $('#initial_value').val();
    var strike = $('#strike').val();
    var volatility = $('#volatility').val();
    var frequency = $('#frequency').val();
    var csr = $('#csr').val();
    var paths = $('#paths').val();

    var currency = $('#currency').val();
    var option_currency = $('#option_currency').val();

    $.ajax({
        type : 'post',
        url: '/options/gbm_json/',
        async:false,
        data: {
            pricing_date_y: pricing_date_y,
            pricing_date_m: pricing_date_m,
            pricing_date_d: pricing_date_d,
            maturity_date_y: maturity_date_y,
            maturity_date_m: maturity_date_m,
            maturity_date_d: maturity_date_d,
            final_date_y: final_date_y,
            final_date_m: final_date_m,
            final_date_d: final_date_d,
            initial_value: initial_value,
            strike: strike,
            volatility: volatility,
            frequency: frequency,
            csr: csr,
            paths: paths,
            currency: currency,
            option_currency: option_currency,

        },
        dataType : 'json',
        success: function(data) {
            chart1.series[1].setData(data.instrument_values);
            chart2.xAxis[0].update({categories: data.time_list});

            random_path = data.random_path;

            call_all_options_values = data.call_all_options_values;
            call_options_value = data.call_options_value;
            put_all_options_values = data.put_all_options_values;
            put_options_value = data.put_options_value;

            s_list = data.s_list;
            call_p_list = data.call_p_list;
            call_d_list = data.call_d_list;
            call_v_list = data.call_v_list;
            put_p_list = data.put_p_list;
            put_d_list = data.put_d_list;
            put_v_list = data.put_v_list;

            // console.log(call_options_value)

        },
        cache: false
    });
}


// ******************************************************************************************************
// 从API获取gbm模拟的10条路径

var num_list = [];
for(var i = 0; i < 100; i++){
    num_list.push(i)
}

function get_gbm_data_path() {
    //从0-99中随机选择10个数，作为路径系数
    //原数组 1 -100
    var arr = [];
    for(var i = 0; i < 100; i++){
        arr.push(i)
    }
    //输出数组
    var out = []
    //输出个数
    var num = 10;
    while(out.length < num){
        var temp = (Math.random()*arr.length) >> 0;
        out.push(arr.splice(temp,1));
    }
    // alert(out);

    // 为chart2添加数据
    for(var i=0; i<10; i++)
        chart2.series[i].setData(random_path[out[i]])
    // console.log(random_path[1])
    // chart2.series[0].setData(ret.path_list)
    // chart2.xAxis[0].update({categories: ret.time_list})

}

var chart2= Highcharts.chart('container_2', {
	chart2: {
		type: 'spline',
        events: {
            load: get_gbm_data_path // 图表加载完毕后执行的回调函数
        },
	},
	title: {
		text: ''
	},
    legend: {
			enabled: false
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
		series: {
			// 针对所有数据列有效
			lineWidth: 1,
            marker: {
			    symbol: 'circle',
                radius: 1,
                enabled: false
		    },
		},
	},
    series: [{
		name: 'Path_0',
		data: [4,5,6,9]
    }, {
		name: 'Path_1',
		data: [4,5,6,9]
    },{
		name: 'Path_2',
		data: [4,5,6,9]
    },{
		name: 'Path_3',
		data: [4,5,6,9]
    },{
		name: 'Path_4',
		data: [4,5,6,9]
    },{
		name: 'Path_5',
		data: [4,5,6,9]
    },{
		name: 'Path_6',
		data: [4,5,6,9]
    },{
		name: 'Path_7',
		data: [4,5,6,9]
    },{
		name: 'Path_8',
		data: [4,5,6,9]
    },{
		name: 'Path_9',
		data: [4,5,6,9]
    },
    ],
    credits:{enabled:false},
});


// ******************************************************************************************************
// 绘制看涨期权价格情况

var chart3 = null;

$(document).ready(function() {
    chart3 = Highcharts.chart('container_3', {
    title: {
        text: ''
    },
    xAxis: [{
        title: { text: '数据点' },
        }, {
        title: { text: '价格' },
        opposite: true,

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
        data: [0.0,
 2.7129206473529415,
 4.025009257559008,
 7.018983487893158,
 0.0,
 0.0,
 0.0,
 0.0,
 10.615782816325307,
 0.0,
 0.0,
 0.0,
 1.2723519103542347,
 10.384368850226393,
 0.0,
 0.0,
 9.373663758809693,
 10.245780131522004,
 0.0,
 0.0],
        id: 's1',
        marker: {
            radius: 0.5
        }}
    ],
    credits:{enabled:false}
    });
})


function set_call_values() {
    chart3.series[1].setData(call_all_options_values);
    chart3.xAxis[1].update({plotLines: [{
                                color: '#FF0000',
                                width: 5,
                                value: call_options_value,
                                zIndex:99,
                                label: {
                                        text: '    欧式看涨期权价值为： '+call_options_value.toString(),
                                        align: 'left',  // 决定定位点
                                        rotation:0,
                                        x: 20,
                                        verticalAlign: 'middle',
                                        style: {
                                            fontWeight: 'bold',
                                            fontSize: '15',
                                        }
                                    }
		                        }],
                            max: call_options_value*3 ,
                            },)
}


// ******************************************************************************************************
// 绘制看涨期权价格S与K

function call_S_K() {
    chart3_1.series[0].setData(call_p_list);
    chart3_1.xAxis[0].update({categories: s_list})
}

var chart3_1= Highcharts.chart('container_3_1', {
	chart3_1: {
		type: 'spline',
	},
	title: {
		text: ''
	},
    legend: {
			enabled: false
    },
	xAxis: {
		categories: [1,2,3,],
        title: {text:'标的资产现价'}
	},
	yAxis: {
		title: {
			text: '期权价格'
		},
	},
	tooltip: {
		crosshairs: true,
		shared: true
	},
	plotOptions: {
		series: {
			lineWidth: 1,
            marker: {
			    symbol: 'circle',
                radius: 1,
                enabled: false
		    },
		},
	},
    series: [{
		name: '欧式看涨期权',
		data: [4,5,6,9]
    }],
    credits:{enabled:false},
});


// ******************************************************************************************************
// 绘制看涨期权价格S与德尔塔

function call_S_D() {
    chart3_2.series[0].setData(call_d_list);
    chart3_2.xAxis[0].update({categories: s_list})
}

var chart3_2= Highcharts.chart('container_3_2', {
	chart3_2: {
		type: 'spline',
	},
	title: {
		text: ''
	},
    legend: {
			enabled: false
    },
	xAxis: {
		categories: [1,2,3,],
        title: {text:'标的资产现价'}
	},
	yAxis: {
		title: {
			text: '期权Delta'
		},
	},
	tooltip: {
		crosshairs: true,
		shared: true
	},
	plotOptions: {
		series: {
			lineWidth: 1,
            marker: {
			    symbol: 'circle',
                radius: 1,
                enabled: false
		    },
		},
	},
    series: [{
		name: '欧式看涨期权Delta',
		data: [4,5,6,9]
    }],
    credits:{enabled:false},
});


// ******************************************************************************************************
// 绘制看涨期权价格S与微咖

function call_S_V() {
    chart3_3.series[0].setData(call_v_list);
    chart3_3.xAxis[0].update({categories: s_list})
}

var chart3_3= Highcharts.chart('container_3_3', {
	chart3_3: {
		type: 'spline',
	},
	title: {
		text: ''
	},
    legend: {
			enabled: false
    },
	xAxis: {
		categories: [1,2,3,],
        title: {text:'标的资产现价'}
	},
	yAxis: {
		title: {
			text: '期权Vega'
		},
	},
	tooltip: {
		crosshairs: true,
		shared: true
	},
	plotOptions: {
		series: {
			lineWidth: 1,
            marker: {
			    symbol: 'circle',
                radius: 1,
                enabled: false
		    },
		},
	},
    series: [{
		name: '欧式看涨期权Vega',
		data: [4,5,6,9]
    }],
    credits:{enabled:false},
});

// ******************************************************************************************************
// 绘制看跌期权价格情况

var chart4 = null;

$(document).ready(function() {
    chart4 = Highcharts.chart('container_4', {
    title: {
        text: ''
    },
    xAxis: [{
        title: { text: '数据点' },
        }, {
        title: { text: '价格' },
        opposite: true,

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
        data: [0.0,
 2.7129206473529415,
 4.025009257559008,
 7.018983487893158,
 0.0,
 0.0,
 0.0,
 0.0,
 10.615782816325307,
 0.0,
 0.0,
 0.0,
 1.2723519103542347,
 10.384368850226393,
 0.0,
 0.0,
 9.373663758809693,
 10.245780131522004,
 0.0,
 0.0],
        id: 's1',
        marker: {
            radius: 0.5
        }}
    ],
    credits:{enabled:false}
    });
})


function set_put_values() {
    chart4.series[1].setData(put_all_options_values);
    chart4.xAxis[1].update({plotLines: [{
                                color: '#FF0000',
                                width: 5,
                                value: put_options_value,
                                zIndex:99,
                                label: {
                                        text: '    欧式看跌期权价值为： '+put_options_value.toString(),
                                        align: 'left',  // 决定定位点
                                        rotation:0,
                                        x: 20,
                                        verticalAlign: 'middle',
                                        style: {
                                            fontWeight: 'bold',
                                            fontSize: '15',
                                        }
                                    }
		                        }],
                            max: put_options_value*3 ,
                            },)
}


// ******************************************************************************************************
// 绘制看跌期权价格S与K

function put_S_K() {
    chart4_1.series[0].setData(put_p_list);
    chart4_1.xAxis[0].update({categories: s_list})
}

var chart4_1= Highcharts.chart('container_4_1', {
	chart4_1: {
		type: 'spline',
	},
	title: {
		text: ''
	},
    legend: {
			enabled: false
    },
	xAxis: {
		categories: [1,2,3,],
        title: {text:'标的资产现价'}
	},
	yAxis: {
		title: {
			text: '期权价格'
		},
	},
	tooltip: {
		crosshairs: true,
		shared: true
	},
	plotOptions: {
		series: {
			lineWidth: 1,
            marker: {
			    symbol: 'circle',
                radius: 1,
                enabled: false
		    },
		},
	},
    series: [{
		name: '欧式看跌期权',
		data: [4,5,6,9]
    }],
    credits:{enabled:false},
});


// ******************************************************************************************************
// 绘制看跌期权价格S与德尔塔

function put_S_D() {
    chart4_2.series[0].setData(put_d_list);
    chart4_2.xAxis[0].update({categories: s_list})
}

var chart4_2= Highcharts.chart('container_4_2', {
	chart4_2: {
		type: 'spline',
	},
	title: {
		text: ''
	},
    legend: {
			enabled: false
    },
	xAxis: {
		categories: [1,2,3,],
        title: {text:'标的资产现价'}
	},
	yAxis: {
		title: {
			text: '期权Delta'
		},
	},
	tooltip: {
		crosshairs: true,
		shared: true
	},
	plotOptions: {
		series: {
			lineWidth: 1,
            marker: {
			    symbol: 'circle',
                radius: 1,
                enabled: false
		    },
		},
	},
    series: [{
		name: '欧式看跌期权Delta',
		data: [4,5,6,9]
    }],
    credits:{enabled:false},
});

// ******************************************************************************************************
// 绘制看跌期权价格S与微咖

function put_S_V() {
    chart4_3.series[0].setData(put_v_list);
    chart4_3.xAxis[0].update({categories: s_list})
}

var chart4_3= Highcharts.chart('container_4_3', {
	chart4_3: {
		type: 'spline',
	},
	title: {
		text: ''
	},
    legend: {
			enabled: false
    },
	xAxis: {
		categories: [1,2,3,],
        title: {text:'标的资产现价'}
	},
	yAxis: {
		title: {
			text: '期权Vega'
		},
	},
	tooltip: {
		crosshairs: true,
		shared: true
	},
	plotOptions: {
		series: {
			lineWidth: 1,
            marker: {
			    symbol: 'circle',
                radius: 1,
                enabled: false
		    },
		},
	},
    series: [{
		name: '欧式看跌期权Vega',
		data: [4,5,6,9]
    }],
    credits:{enabled:false},
});