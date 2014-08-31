# -*- coding: utf-8 -*-

require "net/http"

def rtx_notify(title, msg, receivers)
  receivers = receivers.join(",")
  uri = URI('http://rtx.me4399.com:8012/sendNotify.cgi')
  params = {:title=>title.encode!("GB18030"),
            :msg=>msg.encode!("GB18030"),
            :receiver=>receivers.force_encoding!("GB18030")}
  uri.query = URI.encode_www_form(params)
  Net::HTTP.get(uri)
end

rtx_notify('测试抬头', '测试正文', ['gz2952', 'gz0145'])
