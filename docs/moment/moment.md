---
title: 轨迹
comments: false  #评论，默认不开启
hide:
  #  - navigation # 隐藏左边导航
   - toc #隐藏右边导
   - feedback
hide_reading_time: true
---

<div id="map-container">
  <iframe src="https://www.google.com/maps/d/embed?mid=1AVORHB2ej9VHyvHXm4p0lQ4qfp22kiU&hl=en&ehbc=2E312F" width="100%" height="500"></iframe>
</div>
<script>
fetch('https://ipapi.co/json/')
  .then(res => res.json())
  .then(data => {
    if (data && data.country_code === 'CN') {
      // 中国大陆IP，隐藏地图
      document.getElementById('map-container').innerHTML = '<p style="text-align:center;color:#888;">请用恰当的姿势本页内容才可见哦！</p>';
    }
  })
  .catch(() => {});
</script>