function click_W() {
  fetch("/data/0cp/naver.html")
  .then((response) => response.text())
  .then((data) => {
      // console.log(data);
      var top_area = document.querySelector(".top_area");
      top_area.innerHTML = data;
  });

  fetch("/data/0cp/test.html")
    .then((response) => response.text())
    .then((data) => {
      data = data.replaceAll("\r", "");
      var dataTable = data.split("\n");

      function color_select(cnt) {
        cnt = Number(cnt);
        if (cnt >= 100) {
          return "red";
        } else if (cnt <= 100 && cnt >= 50) {
          return "blue";
        } else {
          return "green";
        }
      }

      //date
      //date
      //date
      const today = new Date();
      const yesterday = new Date(today);
      yesterday.setDate(yesterday.getDate() - 1);
      today.toDateString();
      show_date = yesterday.toDateString();
      if (show_date.includes("Sun") > 0) {
        show_date = "지난주 금~일 (3일간)";
      }
      show_date = "금~월(26~29) 4일간";

      // show_date = "2023-05-04 ~ 2023-05-07(4일간)"

      var el = document.querySelectorAll("#topbnr");
      el[0].innerHTML =
        el[0].innerHTML + `<p style="font-size:15px;">${show_date}</p>`;

      //first
      //first
      //first
      var filterArray = [];
      var f_text = "alt_행사cate_";
      for (var i = 0; i < dataTable.length; i++) {
        if (dataTable[i].includes(f_text)) {
          var temp = dataTable[i].split(",");
          filterArray.push([
            temp[1].replace("alt_행사cate_", ""),
            temp[2],
          ]);
        }
      }

      var top_slt = document.querySelector(".sec01_left.fleft");
      var top_slt_2 = top_slt.querySelectorAll("li");
      for (var i = 0; i < top_slt_2.length; i++) {
        if (top_slt_2[i].querySelector("img")) {
          var text = top_slt_2[i].querySelector("img").alt;
          for (j = 0; j < filterArray.length; j++) {
            if (text.includes(filterArray[j][0])) {
              top_slt_2[i].querySelector("a").innerText =
                filterArray[j][0] + filterArray[j][1];
              top_slt_2[i].querySelector("a").style.color = color_select(
                filterArray[j][1]
              );
              break;
            }
          }
        } else {
          var text = top_slt_2[i].querySelector("a").innerText;
          for (j = 0; j < filterArray.length; j++) {
            if (text.includes(filterArray[j][0])) {
              top_slt_2[i].querySelector("a").innerText =
                filterArray[j][0] + filterArray[j][1];
              top_slt_2[i].querySelector("a").style.color = color_select(
                filterArray[j][1]
              );
              break;
            }
          }
        }
      }

      //second
      //second
      //second
      var filterArray = [];
      var f_text = "w_btn2_";
      for (var i = 0; i < dataTable.length; i++) {
        if (dataTable[i].includes(f_text)) {
          var temp = dataTable[i].split(",");
          filterArray.push([temp[1], temp[2]]);
        }
      }
      var el0 = document.querySelector(".depth0.gnb_menu0");
      var el = el0.querySelectorAll("li > a");
      for (var i = 0; i < el.length; i++) {
        try {
          var temp = f_text + el[i].innerText;
          for (var j = 0; j < filterArray.length; j++) {
            if (temp === filterArray[j][0]) {
              el[i].innerText = el[i].innerText + filterArray[j][1];
              el[i].style.color = color_select(filterArray[j][1]);
            }
          }
        } catch (error) {
          // console.log(error);
        }
      }

      //third
      //third
      //third
      var filterArray = [];
      var f_text = "alt_메인배너_";
      for (var i = 0; i < dataTable.length; i++) {
        if (dataTable[i].includes(f_text)) {
          var temp = dataTable[i].split(",");
          filterArray.push([temp[1], temp[2]]);
        }
      }
      var el = document.querySelectorAll(
        "div.slider-fix_nav > div > ul > li > a"
      );
      for (var i = 0; i < el.length; i++) {
        try {
          var temp = f_text + el[i].innerText;
          for (var j = 0; j < filterArray.length; j++) {
            if (temp === filterArray[j][0]) {
              el[i].innerText = el[i].innerText + filterArray[j][1];
              el[i].style.color = color_select(filterArray[j][1]);
            }
          }
        } catch (error) {
          // console.log(error);
        }
      }

      //fourth
      //fourth
      //fourth
      var filterArray = [];
      var f_text = "alt_프로모션_";
      for (var i = 0; i < dataTable.length; i++) {
        if (dataTable[i].includes(f_text)) {
          var temp = dataTable[i].split(",");
          filterArray.push([temp[1], temp[2]]);
        }
      }
      var el = document.querySelectorAll(
        "div.main_promotion > div > div > div > div > a > img"
      );
      var el2 = document.querySelectorAll(
        "div.main_promotion > div > div > div > div > a"
      );
      for (var i = 0; i < el.length; i++) {
        try {
          var temp = "alt_" + el[i].alt;
          for (var j = 0; j < filterArray.length; j++) {
            if (temp === filterArray[j][0]) {
              el2[i].innerHTML =
                el2[i].innerHTML + `<p>${filterArray[j][1]}</p>`;
              el2[i].style.color = color_select(filterArray[j][1]);
            }
          }
        } catch (error) {
          // console.log(error);
        }
      }

      //하단 멀티팝업
      //하단 멀티팝업
      //하단 멀티팝업
      var filterArray = [];
      var f_text = "alt_멀티팝업_";
      for (var i = 0; i < dataTable.length; i++) {
        if (dataTable[i].includes(f_text)) {
          var temp = dataTable[i].split(",");
          filterArray.push([temp[1], temp[2]]);
        }
      }
      var el = document.querySelectorAll(
        ".showarea > div > div > div > a > img"
      );
      var el2 = document.querySelectorAll(".showarea > div > div > div > a");
      for (var i = 0; i < el.length; i++) {
        try {
          var temp = "alt_" + el[i].alt;
          for (var j = 0; j < filterArray.length; j++) {
            if (temp === filterArray[j][0]) {
              el2[i].innerHTML =
                el2[i].innerHTML + `<p>${filterArray[j][1]}</p>`;
              el2[i].style.color = color_select(filterArray[j][1]);
            }
          }
        } catch (error) {
          // console.log(error);
        }
      }
    });
}

function click_M() {
  fetch("/data/0cp/naver_m.html")
  .then((response) => response.text())
  .then((data) => {
      // console.log(data);
      var top_area = document.querySelector(".top_area");
      top_area.innerHTML = data;
  });

  fetch("/data/0cp/test.html")
    .then((response) => response.text())
    .then((data) => {
      data = data.replaceAll("\r", "");
      var dataTable = data.split("\n");

      function color_select(cnt) {
        cnt = Number(cnt);
        if (cnt >= 100) {
          return "red";
        } else if (cnt <= 100 && cnt >= 50) {
          return "blue";
        } else {
          return "green";
        }
      }

      //date
      //date
      //date
      const today = new Date();
      const yesterday = new Date(today);
      yesterday.setDate(yesterday.getDate() - 1);
      today.toDateString();
      show_date = yesterday.toDateString();
      if (show_date.includes("Sun") > 0) {
        show_date = "지난주 금~일 (3일간)";
      }
      show_date = "금~월(26~29) 4일간";
      // show_date = "2023-05-04 ~ 2023-05-07(4일간)"


      var el = document.querySelectorAll("#topbnr");
      el[0].innerHTML =
        el[0].innerHTML + `<p style="font-size:15px;">${show_date}</p>`;


      //first
      //first
      //first
      var filterArray = [];
      var f_text = "alt_m_";
      for (var i = 0; i < dataTable.length; i++) {
        if (dataTable[i].includes(f_text)) {
          var temp = dataTable[i].split(",");
          filterArray.push([temp[1], temp[2]]);
        }
      }
      var el = document.querySelectorAll("div.swiper-slide > a");
      for (var i = 0; i < el.length; i++) {
        try {
          var temp = f_text + el[i].innerText;
          for (var j = 0; j < filterArray.length; j++) {
            if (temp === filterArray[j][0]) {
              el[i].innerText = el[i].innerText + filterArray[j][1];
              el[i].style.color = color_select(filterArray[j][1]);
            }
          }
        } catch (error) {
          // console.log(error);
        }
      }

      //second
      //second
      //second
      var filterArray = [];
      var f_text = "alt_메인배너_";
      for (var i = 0; i < dataTable.length; i++) {
        if (dataTable[i].includes(f_text)) {
          var temp = dataTable[i].split(",");
          filterArray.push([temp[1], temp[2]]);
        }
      }
      var el = document.querySelectorAll(
        "div.slider-fix_nav > div > ul > li > a"
      );
      for (var i = 0; i < el.length; i++) {
        try {
          var temp = f_text + el[i].innerText;
          for (var j = 0; j < filterArray.length; j++) {
            if (temp === filterArray[j][0]) {
              el[i].innerText = el[i].innerText + filterArray[j][1];
              el[i].style.color = color_select(filterArray[j][1]);
            }
          }
        } catch (error) {
          // console.log(error);
        }
      }

      //third
      //third
      //third
      var filterArray = [];
      var f_text = "alt_프로모션_";
      for (var i = 0; i < dataTable.length; i++) {
        if (dataTable[i].includes(f_text)) {
          var temp = dataTable[i].split(",");
          filterArray.push([temp[1], temp[2]]);
        }
      }
      var el = document.querySelectorAll(
        "div.event_mini > div > div > div > div > a > img"
      );
      var el2 = document.querySelectorAll(
        "div.event_mini > div > div > div > div > a"
      );

      for (var i = 0; i < el.length; i++) {
        try {
          var temp = "alt_" + el[i].alt;
          for (var j = 0; j < filterArray.length; j++) {
            if (temp === filterArray[j][0]) {
              el2[i].innerHTML =
                el2[i].innerHTML + `<p>${filterArray[j][1]}</p>`;
              el2[i].style.color = color_select(filterArray[j][1]);
            }
          }
        } catch (error) {
          // console.log(error);
        }
      }

      //fourth
      //fourth
      //fourth
      var filterArray = [];
      var f_text = "alt_m_";
      for (var i = 0; i < dataTable.length; i++) {
        if (dataTable[i].includes(f_text)) {
          var temp = dataTable[i].split(",");
          filterArray.push([temp[1], temp[2]]);
        }
      }
      var el = document.querySelectorAll("ul.cate_container > li > a > p");
      for (var i = 0; i < el.length; i++) {
        try {
          var temp = f_text + el[i].innerText;
          for (var j = 0; j < filterArray.length; j++) {
            if (temp === filterArray[j][0]) {
              el[i].innerText = el[i].innerText + "\n" + filterArray[j][1];
              el[i].style.color = color_select(filterArray[j][1]);
            }
          }
        } catch (error) {
          // console.log(error);
        }
      }

      //fifth (nav)
      //fifth (nav)
      //fifth (nav)
      var filterArray = [];
      var nav_list = ["홈", "카테고리", "검색", "장바구니", "마이페이지"];
      var f_text = "alt_m_nav_";
      for (var i = 0; i < dataTable.length; i++) {
        if (dataTable[i].includes(f_text)) {
          var temp = dataTable[i].split(",");
          filterArray.push([temp[1], temp[2]]);
        }
      }
      var el = document.querySelectorAll("#nav_bar > ul > li > a > div");
      for (var i = 0; i < el.length; i++) {
        try {
          var temp = f_text + nav_list[i];
          for (var j = 0; j < filterArray.length; j++) {
            if (temp === filterArray[j][0]) {
              el[i].innerHTML = `<p>${filterArray[j][1]}</p>`;
              el[i].style.color = color_select(filterArray[j][1]);
            }
          }
        } catch (error) {
          // console.log(error);
        }
      }

      //sixth
      //sixth
      //sixth
      var filterArray = [];
      var f_text = "m_btm_eb_";
      for (var i = 0; i < dataTable.length; i++) {
        if (dataTable[i].includes(f_text)) {
          var temp = dataTable[i].split(",");
          filterArray.push([temp[1], temp[2]]);
        }
      }
      var el = document.querySelectorAll("div.event_ban > a > img");
      var el2 = document.querySelectorAll("div.event_ban > a");
      var cnt_ = 0;
      for (i = 0; i < el.length; i++) {
        try {
          if (el[i].alt.includes("m_btm_eb") > 0) {
            el2[i].innerHTML =
              `<p style="font-size:15px;">${filterArray[cnt_][1]}</p>` +
              el2[i].innerHTML;
            el2[i].style.color = color_select(filterArray[cnt_][1]);
            cnt_ += 1;
          }
        } catch (error) {
          // console.log(error);
        }
      }

      //rest
      //rest
      //rest
      var filterArray = [];
      var f_text = "mm_";
      for (var i = 0; i < dataTable.length; i++) {
        if (dataTable[i].includes(f_text)) {
          var temp = dataTable[i].split(",");
          filterArray.push([temp[1], temp[2]]);
        }
      }
      var el = document.getElementsByClassName("t1");
      for (var i = 0; i < el.length; i++) {
        try {
          var temp = f_text + el[i].innerText;
          for (var j = 0; j < filterArray.length; j++) {
            if (temp === filterArray[j][0]) {
              el[i].innerText = el[i].innerText + "\n" + filterArray[j][1];
              el[i].style.color = color_select(filterArray[j][1]);
            }
          }
        } catch (error) {
          // console.log(error);
        }
      }
      //rest위클리딜
      var filterArray = [];
      var f_text = "mm_위클리딜";
      for (var i = 0; i < dataTable.length; i++) {
        if (dataTable[i].includes(f_text)) {
          var temp = dataTable[i].split(",");
          filterArray.push([temp[1], temp[2]]);
        }
      }
      var el = document.querySelector(".main_title.weeklydeal.cboth > .t1");
      el.innerHTML = el.innerHTML + `<p>${filterArray[0][1]}</p>`;
      el.style.color = color_select(filterArray[0][1]);
    });
}

function goodsNo() {
  // Select all <a> tags
  var replay_ck = document.getElementById("insert_code");
  if (replay_ck == null) {
    const links = document.querySelectorAll("a");

    // Loop through each <a> tag and get the value of its href attribute
    links.forEach(function (link, index) {
      const href = link.getAttribute("href");
      var strong_pass = links[index].querySelector("strong");
      var class_name = links[index].getElementsByClassName("ver_middle");
      try {
        if (
          href.includes("goodsNo=") > 0 &&
          (strong_pass == null || class_name.length > 0)
        ) {
          var temp = href.split("goodsNo=")[1];
          if (temp.includes("&") > 0) {
            temp = temp.split("&")[0];
          }
          link.innerHTML =
            `<p id="insert_code" style="font-size:20px;">${temp}</p>` +
            link.innerHTML;
        }
      } catch {
        // console.log(link);
      }
    });
  }
}

function show() {
  goodsNo();

  var ck_WM = window.location.href;
  if (ck_WM.includes("//m.")) {
    click_M();
  } else {
    click_W();
  }
}
