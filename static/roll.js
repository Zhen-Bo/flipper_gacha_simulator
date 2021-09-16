$(function () {
  let uri = window.location.toString();
  if (uri.indexOf("?") > 0) {
    let clean_uri = uri.substring(0, uri.indexOf("?"));
    window.history.replaceState({}, document.title, clean_uri);
  }
  $("#search-index").keyup(function (event) {
    if (
      event.keyCode === 13 &&
      !$("#search-btn").is(":disabled") &&
      $("#search-index").val() != ""
    ) {
      $("#search-btn").click();
    }
  });

  $("#search-btn").click(function () {
    let index = $("#search-index").val();
    $("#search-index").val("");
    if (index != "" && index / 1 > 0) {
      let url = `/wf/result?pool=${$("#pool").val()}&roll=${index}`;
      $("#search-btn").attr("disabled", true);
      location.href = url;
    } else {
      alert("輸入錯誤!");
    }
  });

  if (location.pathname == "/wf/result") {
    $("#roll").find("img").attr("src", "/wf/static/back.png");
  } else {
    $("#roll").find("img").attr("src", "/wf/static/roll.png");
  }

  $("#roll").click(function () {
    if (location.pathname == "/wf/result") {
      location.href = `/wf/flipper?pool=${$("#pool").val()}`;
    } else {
      get_simulation($("#pool").val());
    }
  });
});

function display_reslut(json) {
  $("#sim_desc").text("此結果為這個網站第 " + json[11] + " 次模擬");
  for (let index = 0; index < 10; index++) {
    $("#slot" + index).empty();
    $("#slot" + index).append(
      "<img src='https://raw.githubusercontent.com/Zhen-Bo/flipper_gacha_simulator/main/static/image/chars/" +
        json[index]["id"] +
        "/square_0.png'  style='width: 82px;height: 82px; background-color: white;'>"
    );
    let class_string =
      "p-2 rarity-" + json[index]["rarity"] + " " + json[index]["attri"];
    $("#slot" + index).attr("class", class_string);
  }
  $("#result_table").show();
  $("#five_sum").text(json[10]["5星"]);
  $("#four_sum").text(json[10]["4星"]);
  $("#three_sum").text(json[10]["3星"]);
  $("#all_five").text(json[12]["all_five"]);
  $("#five_rate").text(
    ((json[12]["all_five"] / json[12]["all_roll"]) * 100).toFixed(3) + "%"
  );
  $("#all_four").text(json[12]["all_four"]);
  $("#four_rate").text(
    ((json[12]["all_four"] / json[12]["all_roll"]) * 100).toFixed(3) + "%"
  );
  $("#all_three").text(json[12]["all_three"]);
  $("#three_rate").text(
    ((json[12]["all_three"] / json[12]["all_roll"]) * 100).toFixed(3) + "%"
  );
  $(".Fire").prepend(
    "<img src = 'https://raw.githubusercontent.com/Zhen-Bo/flipper_gacha_simulator/main/static/image/elements/element_red.png' style='width: 20px; height: 20px;position: absolute; top: 0px; right: 0px;background-color:white;'>"
  );
  $(".Water").prepend(
    "<img src = 'https://raw.githubusercontent.com/Zhen-Bo/flipper_gacha_simulator/main/static/image/elements/element_blue.png' style='width: 20px; height: 20px;position: absolute; top: 0px; right: 0px;background-color:white;'>"
  );
  $(".Thunder").prepend(
    "<img src = 'https://raw.githubusercontent.com/Zhen-Bo/flipper_gacha_simulator/main/static/image/elements/element_yellow.png' style='width: 20px; height: 20px;position: absolute; top: 0px; right: 0px;background-color:white;'>"
  );
  $(".Wind").prepend(
    "<img src = 'https://raw.githubusercontent.com/Zhen-Bo/flipper_gacha_simulator/main/static/image/elements/element_green.png' style='width: 20px; height: 20px;position: absolute; top: 0px; right: 0px;background-color:white;'>"
  );
  $(".Light").prepend(
    "<img src = 'https://raw.githubusercontent.com/Zhen-Bo/flipper_gacha_simulator/main/static/image/elements/element_white.png' style='width: 20px; height: 20px;position: absolute; top: 0px; right: 0px;background-color:white;'>"
  );
  $(".Dark").prepend(
    "<img src = 'https://raw.githubusercontent.com/Zhen-Bo/flipper_gacha_simulator/main/static/image/elements/element_black.png' style='width: 20px; height: 20px;position: absolute; top: 0px; right: 0px;background-color:white;'>"
  );
  $(".rarity-5-pu").prepend(
    "<img src='https://i.pinimg.com/originals/0b/28/1b/0b281bc1f36f57e3b865ab2e4bac40ba.gif' style='width:100%;height:100%; position: absolute; top: 0px; right: 0px;'>"
  );
  setTimeout(function () {
    $("#roll").attr("disabled", false);
  }, 800);
}
async function get_simulation(pool) {
  $("#roll").attr("disabled", true);
  let url = "/wf/roll?pool=" + pool;
  for (let index = 0; index < 10; index++) {
    let img_src =
      "https://lpc.opengameart.org/sites/default/files/TransparencyDark640.png";
    $("#slot" + index)
      .find("img")
      .attr("src", img_src);
    $("#slot" + index).attr("class", "p-2");
  }
  try {
    let response = await fetch(url);
    let json = await response.json();
    display_reslut(json);
  } catch (error) {
    console.log("Request Failed", error);
  }
}

function change_information(json) {
  $("#sim_desc").html(
    `此網站已模擬 ${(
      json["all_roll"] / 10
    ).toFixed()} 次<br>請點擊下方按鈕開始模擬`
  );
  for (let index = 0; index < 10; index++) {
    $("#slot" + index).empty();
    $("#slot" + index).append(
      `<img style="width: 82px; height: 82px;" src="https://lpc.opengameart.org/sites/default/files/TransparencyDark640.png">`
    );
    $("#slot" + index).attr("class", "p-2");
  }
  $("#result_table").hide();
  $("#all_five").text(json["all_five"]);
  $("#five_rate").text(
    ((json["all_five"] / json["all_roll"]) * 100).toFixed(3) + "%"
  );
  $("#all_four").text(json["all_four"]);
  $("#four_rate").text(
    ((json["all_four"] / json["all_roll"]) * 100).toFixed(3) + "%"
  );
  $("#all_three").text(json["all_three"]);
  $("#three_rate").text(
    ((json["all_three"] / json["all_roll"]) * 100).toFixed(3) + "%"
  );
  $("#all_roll").text(json["all_roll"]);
  $("#roll_rate").text(
    ((json["all_roll"] / json["all_roll"]) * 100).toFixed(3) + "%"
  );
}

async function switch_pool(pool_id) {
  let url = "/wf/result?pool=" + pool_id + "&data_mode=true";
  try {
    let response = await fetch(url);
    let json = await response.json();
    change_information(json);
  } catch (error) {
    console.log("Request Failed", error);
  }
  $("#pool").attr("disabled", false);
  $("#roll").attr("disabled", false);
  $("#search-btn").attr("disabled", false);
}
