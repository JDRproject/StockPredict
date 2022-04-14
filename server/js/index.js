var stock = stock || {};

stock = {
  common: function () {},
  getContextPath: function() {
	var hostIndex = location.href.indexOf(location.host) + location.host.length;
	return location.href.substring(hostIndex, location.href.indexOf('/', hostIndex + 1));
  },
  onClick: function () {
    var self = this;

    $("form").submit(function (e) {
      e.preventDefault();
        var data = {
          emailAddress: "asdf",
          recoveryEmail: "asdf",
          password: "zxcv",
        };
        $.ajax({
          type: "POST",
          url: stock.getContextPath() + "/api/test",
          dataType: "json",
          contentType: "application/json; charset=utf-8",
          data: JSON.stringify(data),
          success: function (res) {
            console.log(res);
          }
      });
    });
  }
};

function test() {
	var data = {
          emailAddress: "asdf",
          recoveryEmail: "asdf",
          password: "zxcv",
        };
	
	$.ajax({
          type: "POST",
          url: stock.getContextPath() + "/api/test",
          dataType: "json",
          contentType: "application/json; charset=utf-8",
          data: JSON.stringify(data),
          success: function (res) {
			console.log(res.emailAddress);
			$("#hello").text(res);
            console.log(res);
          }
      });
}