<%@ page contentType="text/html;charset=utf-8" pageEncoding="utf-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta http-equiv="expires" content="0">
<meta http-equiv="cache-control" content="no-cache">
<meta http-equiv="pragma" content="no-cache">
<title>Magellan</title>
<link href="<%=request.getContextPath()%>/bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">
<link href="<%=request.getContextPath()%>/css/base.css" rel="stylesheet" media="screen">
<link href="<%=request.getContextPath()%>/font-awesome/css/font-awesome.min.css" rel="stylesheet" media="screen">

<script src="<%=request.getContextPath()%>/js/jquery-1.11.0.min.js"></script>
<script src="<%=request.getContextPath()%>/bootstrap/js/bootstrap.min.js"></script>
<script src="<%=request.getContextPath()%>/js/jquery.cookie.js"></script>
</head>

<body>
	<div class="row">
		<div class="col-md-12">
			<div class="panel panel-primary">
				<div class="panel-heading">
					<h3 class="panel-title">
						<i class="fa fa-book"></i> 订单记录<span class="pull-right">支付单号：<input id="cb2" type="checkbox" checked onclick="toggleColumn(event,2);">&nbsp;&nbsp;&nbsp;支付方式：<input id="cb3" type="checkbox" checked onclick="toggleColumn(event,3);">&nbsp;&nbsp;&nbsp;收件人电话：<input id="cb6" type="checkbox" checked onclick="toggleColumn(event,6);"></span>
					</h3>
				</div>
				<div class="panel-body">
					<table id="orderTable" class="table table-striped table-bordered table-hover tablesorter">
						<thead>
							<tr>
								<th><a href="list.view?sortField=orderTime&orderType=${orderType == 'desc' ? 'asc' : 'desc'}">下单时间<c:if test="${sortField == 'orderTime'}">
											<c:choose>
												<c:when test="${orderType == 'desc'}">
													<i class="fa fa-arrow-down"></i>
												</c:when>
												<c:otherwise>
													<i class="fa fa-arrow-up"></i>
												</c:otherwise>
											</c:choose>
										</c:if></a></th>
								<th>订单号</th>
								<th>支付单号</th>
								<th><a href="query.view?sortField=paymentType&orderType=${orderType == 'desc' ? 'asc' : 'desc'}">支付方式<c:if test="${sortField == 'paymentType'}">
											<c:choose>
												<c:when test="${orderType == 'desc'}">
													<i class="fa fa-arrow-down"></i>
												</c:when>
												<c:otherwise>
													<i class="fa fa-arrow-up"></i>
												</c:otherwise>
											</c:choose>
										</c:if></a></th>
								<th>物流单号</th>
								<th><a href="query.view?sortField=receiver&orderType=${orderType == 'desc' ? 'asc' : 'desc'}">收件人<c:if test="${sortField == 'receiver'}">
											<c:choose>
												<c:when test="${orderType == 'desc'}">
													<i class="fa fa-arrow-down"></i>
												</c:when>
												<c:otherwise>
													<i class="fa fa-arrow-up"></i>
												</c:otherwise>
											</c:choose>
										</c:if></a></th>
								<th>收件人电话</th>
								<th>状态</th>
								<th>操作</th>
							</tr>
						</thead>
						<tbody>
							<c:forEach items="${list}" var="item">
								<tr id="tr-${item.orderCode}">
									<td><fmt:formatDate pattern="yyyy-MM-dd HH:mm:ss" value="${item.orderTime}" /></td>
									<td>${item.orderCode}</td>
									<td>${item.paymentNum}</td>
									<td><c:choose>
											<c:when test="${item.paymentType == 3}">支付宝</c:when>
											<c:when test="${item.paymentType == 4}">微信支付</c:when>
											<c:when test="${item.paymentType == 41}">微信APP</c:when>
											<c:when test="${item.paymentType == 42}">微信公众号</c:when>
											<c:when test="${item.paymentType == 6}">银联支付</c:when>
											<c:when test="${item.paymentType == 7}">支付宝国际</c:when>
											<c:otherwise>其他</c:otherwise>
										</c:choose></td>
									<td>${item.logisticsNum}</td>
									<td>${item.receiver}</td>
									<td>${item.contactPhone}</td>
									<td><c:choose>
											<c:when test="${item.currentState == 100}">
												<i class="fa fa-plus-square"></i>&nbsp;<span class="label label-success">接收订单</span>
											</c:when>
											<c:when test="${item.currentState == 110}">
												<i class="fa fa-exclamation-triangle"></i>&nbsp;<span class="label label-danger">支付报关失败</span>
											</c:when>
											<c:when test="${item.currentState == 111}">
												<i class="fa fa-spinner"></i>&nbsp;<span class="label label-info">支付报关进行中</span>
											</c:when>
											<c:when test="${item.currentState == 119}">
												<i class="fa fa-check-square-o"></i>&nbsp;<span class="label label-success">支付报关完成</span>
											</c:when>
											<c:when test="${item.currentState == 120}">
												<i class="fa fa-exclamation-triangle"></i>&nbsp;<span class="label label-danger">国检订单申报失败</span>
											</c:when>
											<c:when test="${item.currentState == 121}">
												<i class="fa fa-spinner"></i>&nbsp;<span class="label label-info">国检订单申报进行中</span>
											</c:when>
											<c:when test="${item.currentState == 129}">
												<i class="fa fa-check-square-o"></i>&nbsp;<span class="label label-success">国检订单申报完成</span>
											</c:when>
											<c:when test="${item.currentState == 130}">
												<i class="fa fa-exclamation-triangle"></i>&nbsp;<span class="label label-danger">海关订单申报失败</span>
											</c:when>
											<c:when test="${item.currentState == 131}">
												<i class="fa fa-spinner"></i>&nbsp;<span class="label label-info">海关订单申报进行中</span>
											</c:when>
											<c:when test="${item.currentState == 139}">
												<i class="fa fa-check-square-o"></i>&nbsp;<span class="label label-success">海关订单申报完成</span>
											</c:when>
											<c:when test="${item.currentState == 140}">
												<i class="fa fa-exclamation-triangle"></i>&nbsp;<span class="label label-danger">物流单对接失败</span>
											</c:when>
											<c:when test="${item.currentState == 149}">
												<i class="fa fa-check-square"></i>&nbsp;<span class="label label-success">物流单对接完成</span>
											</c:when>
											<c:when test="${item.currentState == 200}">
												<span class="label label-info">待发货</span>
											</c:when>
											<c:when test="${item.currentState == 210}">
												<i class="fa fa-university"></i>&nbsp;<span class="label label-success">进境清关</span>
											</c:when>
											<c:when test="${item.currentState == 211}">
												<i class="fa fa-exclamation-triangle"></i>&nbsp;<span class="label label-info">进境清关失败</span>
											</c:when>
											<c:when test="${item.currentState == 220}">
												<span class="label label-info">正在打包</span>
											</c:when>
											<c:when test="${item.currentState == 230}">
												<span class="label label-info">保税区出仓</span>
											</c:when>
											<c:when test="${item.currentState == 300}">
												<i class="fa fa-truck"></i>&nbsp;<span class="label label-info">已发货</span>
											</c:when>
											<c:when test="${item.currentState == 400}">
												<i class="fa fa-anchor"></i>&nbsp;<span class="label label-success">订单完成</span>
											</c:when>
											<c:when test="${item.currentState == 500}">
												<i class="fa fa-undo"></i>&nbsp;<span class="label label-warning">申请退单</span>
											</c:when>
											<c:when test="${item.currentState == 600}">
												<i class="fa fa-anchor"></i>&nbsp;<span class="label label-default">退单完成</span>
											</c:when>
											<c:when test="${item.currentState == 700}">
												<i class="fa fa-trash"></i>&nbsp;<span class="label label-default">中止作废</span>
											</c:when>
											<c:otherwise>
												<i class="fa fa-bug"></i>&nbsp;<span class="label label-danger">异常</span>
											</c:otherwise>
										</c:choose></td>
									<td>
										<button class="btn btn-xs btn-info" title="明细" onclick="detail('${item.orderCode}')">
											<i class="fa fa-list"></i>
										</button>&nbsp;
										<button class="btn btn-xs btn-warning" title="编辑" onclick="">
											<i class="fa fa-pencil"></i>
										</button>&nbsp;
										<button class="btn btn-xs btn-danger" title="删除" onclick="">
											<i class="fa fa-times"></i>
										</button>
									</td>
								</tr>
							</c:forEach>
						</tbody>
					</table>
					<div class="text-right">
						<ul class="pagination pull-right">${pageHtml}</ul>
					</div>
				</div>
			</div>
		</div>
	</div>
	<script>
	function toggleColumn(e, i){
		var t = e.target.checked;
		var e = $('#orderTable tr').find('th:eq(' + i + '),td:eq(' + i +')');
		if(t === true){
			e.show();
		} else {
			e.hide();
		}
		$.cookie('td' + i, t === true ? 1 : 0, {expires:365, path:'/'});
	}
	
    function detail(id) {
        window.location.href = "detail.view?id=" + id
    }
	
    function edit(id) {
        window.location.href = "edit.view?id=" + id
    }

    function del(id) {
        $.post("<%=request.getContextPath()%>/order/delete.do", {"id" : id}, function(json) {
				if (json.result === true) {
					$('#tr-' + json.id).remove();
					window.location.reload();
				} else {
					alert('删除失败');
				}
			});
		}

		$(function() {
			var arr = [ 2, 3, 6];
			for (var i = 0; i < arr.length; i++) {
				var v = arr[i];
				var t = $.cookie('td' + v);
				if (t == 0) {
					$('#cb' + v).attr("checked", false);
					$('#orderTable tr').find('th:eq(' + v + '),td:eq(' + v + ')').hide();
				}
			}
		});
	</script>
</body>
</html>