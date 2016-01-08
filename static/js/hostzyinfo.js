  /**
 * Created by DELL on 2015/12/5.
 */
    //var cpuinfo=document.getElementById("cpuinfo").innerText
    //var cpuclock=document.getElementById("cpuclock").innerHTML
    //alert(cpuinfo+"ppp"+cpuclock);
        require.config({
            paths: {
                echarts: '/static/js/dist'
            }
        });
        require(
            [
                'echarts',
                'echarts/chart/line',   // 按需加载所需图表，如需动态类型切换功能，别忘了同时加载相应图表
                'echarts/chart/pie'
            ],
                 function (ec) {
                var myChart = ec.init(document.getElementById('vsum'));
                var option = {
    title : {
        text: '主机资源使用',
        subtext: ''
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['CPU资源使用']
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'category',
            boundaryGap : false,

            data:[{% for value in cpuclock %}
                        '{{ value }}',
                    {% endfor %}
            ]
{#            data:['02:46:54', '02:47:54', '02:48:54', '02:49:54', '02:50:54']#}
        }
    ],
    yAxis : [
        {
            type : 'value',
            axisLabel : {
                formatter: '{value} '
            }
        }
    ],
    series : [
        {
            name:'CPU资源使用',
            type:'line',

            data:[{% for value in cpuinfo %}
                        {{ value }},
                    {% endfor %}
                    ],
            markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                ]
            },
            markLine : {
                data : [
                    {type : 'average', name: '平均值'}
                ]
            }
        },
    ]
};
                myChart.setOption(option);
            }
        );




