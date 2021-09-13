$(function () {
  $("#search-index").keyup(function (event) {
    if (event.keyCode === 13) {
      $("#search-btn").click();
    }
  });
  $("#search-btn").click(function () {
    let index = $("#search-index").val();
    let url = "/wf/result?roll=" + index;
    location.href = url;
  });
  if (location.pathname == "/wf/result") {
    $("#roll").find("img").attr("src", "/static/flipper_gacha/back.png");
  } else {
    $("#roll").find("img").attr("src", "/static/flipper_gacha/roll.png");
  }
  $("#roll").click(function () {
    if (location.pathname == "/wf/result") {
      location.href = "/wf/flipper";
    } else {
      get_simulation();
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
async function get_simulation() {
  $("#roll").attr("disabled", true);
  let url = "/wf/roll";
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
