// url
const FREENOM = 'https://my.freenom.com'
const CLIENT_AREA = `${FREENOM}/clientarea.php`
const LOGIN_URL = `${FREENOM}/dologin.php`
const DOMAIN_STATUS_URL = `${FREENOM}/domains.php?a=renewals`
const RENEW_REFERER_URL = `${FREENOM}/domains.php?a=renewdomain`
const RENEW_DOMAIN_URL = `${FREENOM}/domains.php?submitrenewals=true`

// default headers
const headers = {
   'content-type': 'application/x-www-form-urlencoded',
   'user-agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/103.0.5060.134 Safari/537.36',
}

async function login() {
   headers['referer'] = CLIENT_AREA
   const resp = await fetch(LOGIN_URL, {
      method: 'POST',
      body: `username=${SECRET_USERNAME}&password=${SECRET_PASSWORD}`,
      headers: headers,
      redirect: 'manual',
   })
   const setCookie = resp.headers
      .get('set-cookie')
      .replace(/([Hh]ttp[Oo]nly(,|)|([Pp]ath|expires|Max-Age)=.*?;)/g, '')
      .replace('WHMCSUser=deleted;', '')
      .replace(/\s+/g, '')
      .split(';')
      .reduce((pre, cur) => {
         const [k, v] = cur.split('=')
         if (k && v) pre[k] = v
         return pre
      }, {})
   const cookie = []
   for (const key in setCookie) {
      cookie.push(`${key}=${setCookie[key]}`)
   }
   return cookie.join(';')
}

async function getDomainInfo() {
   const res = { token: null, domains: {} }
   // request
   headers['referer'] = CLIENT_AREA
   const resp = await fetch(DOMAIN_STATUS_URL, { headers: headers })
   const html = await resp.text()
   // login check
   if (/<a href="logout.php">Logout<\/a>/i.test(html) == false) {
      console.error('get login status failed')
      return res
   }
   // get page token
   const tokenMatch = /name="token" value="(.*?)"/i.exec(html)
   if (tokenMatch.index == -1) {
      console.error('get page token failed')
      return res
   }
   res.token = tokenMatch[1]
   // get domains
   for (const item of html.match(/<tr>[^&]+&domain=.*?<\/tr>/g)) {
      const domain = /<tr><td>(.*?)<\/td><td>[^<]+<\/td><td>/i.exec(item)[1]
      const days = /<span[^>]+>(\d+).Days<\/span>/i.exec(item)[1]
      const renewalId = /[^&]+&domain=(\d+?)"/i.exec(item)[1]
      res.domains[domain] = { days, renewalId }
   }
   return res
}

async function renewDomains(domainInfo) {
   const token = domainInfo.token
   for (const domain in domainInfo.domains) {
      const days = domainInfo.domains[domain].days
      if (parseInt(days) < 14) {
         const renewalId = domainInfo.domains[domain].renewalId
         headers['referer'] = `${RENEW_REFERER_URL}&domain=${renewalId}`
         const resp = await fetch(RENEW_DOMAIN_URL, {
            method: 'POST',
            body: `token=${token}&renewalid=${renewalId}&renewalperiod[${renewalId}]=12M&paymentmethod=credit`,
            headers: headers,
         })
         const html = await resp.text()
         console.log(
            domain,
            /Order Confirmation/i.test(html) ? 'Renewal Success' : 'Renewal Failed'
         )
      } else {
         console.log(`Domain ${domain} still has ${days} days until renewal.`)
      }
   }
}

async function handleSchedule(scheduledDate) {
   console.log('scheduled date', scheduledDate)
   const cookie = await login()
   console.log('cookie', cookie)
   headers['cookie'] = cookie
   const domainInfo = await getDomainInfo()
   console.log('token', domainInfo.token)
   console.log('domains', domainInfo.domains)
   await renewDomains(domainInfo)
}

addEventListener('scheduled', (event) => {
   event.waitUntil(handleSchedule(event.scheduledTime))
})


async function sendMessage(message) {
  if (typeof TGBOT_TOKEN === "undefined" || typeof TGBOT_CHAT_ID === "undefined") {
    console.log("发送失败");
    return;
  }

  const response = await retryFetch(`https://api.telegram.org/bot${TGBOT_TOKEN}/sendMessage`, {
    method: "post",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      chat_id: TGBOT_CHAT_ID,
      text: message
    })
  });
  if (response.status !== 200) {
    console.error(await response.text());
  }
}


function retry(fn, times = 3, delay = 1000) {
  return async (...args) => {
    for (let i = 0; i < times; i++) {
      try {
        return await fn(...args);
      } catch (e) {
        console.error(`Retry: #${i} ${e.message}`);
        await sleep(delay);
      }
    }
    console.error("Failed to execute");
  }
}

function retryFetch(url, options) {
  return retry(fetch)(url, options);
}


async function GetDataInfo() {
  const d = new Date(); 
  //得到1970年一月一日到现在的秒数 
  const len = d.getTime();
  //本地时间与GMT时间的时间偏移差(注意：GMT这是UTC的民间名称。GMT=UTC）
  const offset = d.getTimezoneOffset() * 60000;
  //得到现在的格林尼治时间
  const utcTime = len + offset;
  const  now=new Date(utcTime + 3600000 * 8);
  const year = now.getFullYear(); //得到年份
  const month = now.getMonth()+1;//得到月份
  const date = now.getDate();//得到日期
  // const day = now.getDay();//得到周几
  const hour= now.getHours();//得到小时数
  const minute= now.getMinutes();//得到分钟数
  const second= now.getSeconds();//得到秒数
  const datta=`${year}-${month}-${date} ${hour}:${minute}`
  return datta
}






async function handleRequest() {
   const cookie = await login()
   console.log('cookie', cookie)
   headers['cookie'] = cookie
   const domainInfo = await getDomainInfo()
   const GetDataI = await GetDataInfo()
   var ReturnMessageTitle="";
   ReturnMessageTitle +=`💖💖Freenoom续期脚本💖💖\n`
   ReturnMessageTitle +=`💸💸💸${GetDataI}💸💸💸\n`
   const domains = domainInfo.domains
   const domainHtml = []
   const TGpush = []
   for (const domain in domains) {
      const days = domains[domain].days
      domainHtml.push(`<p>Domain ${domain} still has ${days} days until renewal.</p>`)
		ReturnMessageTitle += `域名 ${domain} 还有 ${days} 天更新\n`;
      // TGpush.push(`域名 ${domain} 还有 ${days} 天 更新`)
	  
   }
   const html = `
   <!DOCTYPE html>
   <html>
   <head><title>Freenom-Workers Renew</title></head>
   <body>
   Project Repository：https://github.com/PencilNavigator/Freenom-Workers<br/>
   ${domainHtml.join('')}
   </body>
   </html>
   `
   await sendMessage(ReturnMessageTitle);
   return new Response(html, {
      headers: { 'content-type': 'text/html; charset=utf-8' },
   })
}

addEventListener('fetch', (event) => {
   event.respondWith(handleRequest())
})
