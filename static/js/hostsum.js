/**
 * Created by DELL on 2015/12/5.
 */
var vhost=document.getElementById('vhost').innerText;
var whost=document.getElementById('whost').innerText;

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
                var myChart = ec.init(document.getElementById('main'));
                var option = {
    title : {
        text: '服务器数量统计',
        subtext: '',
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
        orient : 'vertical',
        x : 'left',
        data:['物理主机','虚拟主机']
    },
    toolbox: {
        show : false,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {
                show: true,
                type: ['pie', 'funnel'],
                option: {
                    funnel: {
                        x: '25%',
                        width: '50%',
                        funnelAlign: 'left',
                        max: 1548
                    }
                }
            },
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    series : [
        {
            name:'访问来源',
            type:'pie',
            radius : '55%',
            center: ['50%', '60%'],
            data:[
                {value:vhost, name:'物理主机'},
                {value:whost, name:'虚拟主机'},

            ]
        }
    ]
};
                myChart.setOption(option);
            }
        );
