//引用superagent包，用于服务器发送http请求
const request = require('superagent')
//导入cheerio包 解析http
const cheerio = require('cheerio')
//导入 art-template
const template = require('art-template')
//导入PATH
const path = require('path')
//导入nodemaler发送邮件的包
const nodemailer = require('nodemailer')
//导入定时任务包
var schedule = require('node-schedule')

function getDate() {
  return new Promise((resolve, reject) => {
    //现在的时间
    const today = new Date()
    //认识的时间
    const meet = new Date('2018-6-13')//自行替换日期
    //认识的天数
    const count = Math.floor((today - meet) / 1000 / 60 / 60 / 24)
    //今天的日期
    const format =
      today.getFullYear() +
      ' / ' +
      (today.getMonth() + 1) +
      ' / ' +
      today.getDate()
    const dayDate = {
      count,
      format,
    }
    resolve(dayDate)
  })
}
// getDate()

//请求墨迹天气的数据
function getMojiData() {
  return new Promise((resolve, reject) => {
    request
      .get('https://tianqi.moji.com/tommorrow/china/guangdong/guangzhou')
      .end((err, res) => {
        if (err) return console.log('数据请求失败')
        const $ = cheerio.load(res.text)
        //温度
        const wendu =
          $('.detail_weather em:eq(0)').text() +
          '-' +
          $('.detail_weather em:eq(1)').text()
        //天气
        const weather = $('.detail_weather span').text()
        //提示
        const tips = $('.detail_ware_title span').text()
        const img = $('.detail_future_grid li.active img:eq(0)').attr("src")
        //墨迹对象
        const mojiData = {
          weather,
          wendu,
          tips,
          img
        }
        resolve(mojiData)
      })
  })
}
// getMojiData()

//请求One页面抓取数据
function getOneData() {
  return new Promise((resolve, reject) => {
    request.get('http://wufazhuce.com/').end((res, err) => {
      if (err) return console.log('数据请求失败')
      //把返回值中的数据解析成HTML
      const $ = cheerio.load(res.text)
      //抓取One的图片
      const img = $('.carousel-inner>.item>img, .carousel-inner>.item>a>img')
        .eq(0)
        .attr('src')
      //抓取One的文本
      const text = $('.fp-one .fp-one-cita-wrapper .fp-one-cita a').eq(0).text()

      const OneData = {
        img,
        text,
      }
      resolve(OneData)
    })
  })
}

// getOneData()

//渲染邮件
async function renderTemplate() {
  //获取日期数据
  const dayData = await getDate()
  //获取墨迹天气数据
  const mojiData = await getMojiData()
  //获取One数据
  const oneData = 1//await getOneData()
  return new Promise((resolve, reject) => {
    const html = template(path.join(__dirname, './mail.html'), {
      dayData,
      mojiData,
      oneData,
    })
    resolve({ html, mojiData })
  })
}

// renderTemplate();

async function sendMail() {
  const { html, mojiData } = await renderTemplate()

  let transporter = nodemailer.createTransport({
    host: 'smtp.163.com',
    port: 465,
    secure: true, // true for 465, false for other ports
    auth: {
      user: 'lingoing0417@163.com', // 你的邮箱账号
      pass: 'BXRNZYKLUQUVCOXT', //你的邮箱的授权码，记得开通SMTP
    },
  })

  // send mail with defined transport object
  let mailOptions = {
    from: '"帅气的开发者" <lingoing0417@163.com>', // 你的邮箱发件人及地址
    to: '2655059397@qq.com', // 对象的邮箱地址
    subject: `温度:${mojiData.wendu} 天气:${mojiData.weather}`, // 副标题
    html: html, // html主体文件
  }

  transporter.sendMail(mailOptions, (error, info = {}) => {
    if (error) {
      sendMail()
    }
    console.log('发送成功', info.messageId)
    console.log('等待下一次发送！')
  })
}
// sendMail()
//定时任务,每天晚上九点.
//var j = schedule.scheduleJob('0 0 21 * * *', function () {
//  sendMail()
//  console.log('定时任务执行完毕!')
//})
async function run() {
  sendMail()
  console.log('发送完毕!')
}
run()
