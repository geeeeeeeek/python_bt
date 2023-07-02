

function ajaxp(a) {
	var b = {
		id: mid,
		action: a
	};
	$.post("/Magnet/ajaxp", b, function(a) {
		"true" == a ? "good" == b.action && (alert("操作成功"), a = $("#goodnum").html(), a++, $("#goodnum").html(a)) : alert("您不能重复操作")
	})
}

function report() {
	layer.open({
		type: 1,
		btn: ['确认', '取消'],
		title: '违规举报',
		anim: 1,
		yes: function(index, layero) {
			$.post("/Magnet/report", {
				id: mid,
				verify: $('#vcode').val()
			}, function(a) {
				layer.closeAll();
				if ("error" == a) {
					alert("验证码错误");
				} else {
					alert("操作成功，此链接已被屏蔽");
					window.location.reload();
				}
			})
		},
		content: '<div class="vcode-box"><img src="/Magnet/verify" onclick="this.src=\'/Magnet/verify?\'+Math.random();"><input type="vcode" id ="vcode" value="" placeholder="防止功能滥用，请输入验证码"></div>'
	});
}

function get_hits() {
	$.get("/Hits/show/id/" + mid, function(a) {
		$("#hits_num").text(a)
	})
}
$(function() {
	var a = new ClipboardJS("#copyi");
	a.on("success", function(a) {
		alert("复制成功!");
		a.clearSelection()
	});
	a.on("error", function(a) {
		alert("复制失败!")
	});
	setTimeout("get_hits()", 120000)
});