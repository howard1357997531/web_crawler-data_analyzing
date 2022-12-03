$(document).ready(function () {
  $(document).on("click", ".newBtn", function () {
    let url = $(this).data("url");
    console.log(url);
    $.ajax({
      url: "/get_url",
      data: {
        url: url,
      },
      dataType: "json",
      success: function (res) {
        $(".applenew_data").html(res.datas);
      },
    });
  });
  $(document).on("click", "#addCity", function () {
    var city = $(".selector").val(); //獲取當前選中項的value
    console.log(city);
    $.ajax({
      url: "/get_city",
      data: {
        city: city,
      },
      dataType: "json",
      success: function (res) {
        console.log(res.data);
        $("#ajaxtable").html(res.data);
      },
    });
  });

  $(document).on("click", "#taiwan_railwayBtn", function () {
    var start_station = $("#start_station").val(); //獲取當前選中項的value
    var end_station = $("#end_station").val();
    var date = $("#date").val();
    var start_time = $("#start_time").val();
    var end_time = $("#end_time").val();
    console.log(start_station, end_station, date, start_time, end_time);

    $.ajax({
      url: "/get_taiwan_railway_data",
      data: {
        start_station: start_station,
        end_station: end_station,
        date: date,
        start_time: start_time,
        end_time: end_time,
      },
      dataType: "json",
      success: function (res) {
        console.log(res.data);
        $("#ajaxtable").html(res.data);
      },
    });
  });

  $(document).on("click", "#nbaBtn", function () {
    let date = $("#date").val();
    console.log(date);
    $.ajax({
      url: "/get_nba_data",
      data: {
        date: date,
      },
      dataType: "json",
      success: function (res) {
        $("#nbadata").html(res.data);
      },
    });
  });
});
