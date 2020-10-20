# -*- coding: utf-8 -*-

import xlrd
from urllib import parse
#from MyPlatform.settings import MEDIA_ROOT


jsRet = 'http://s.click.taobao.com/t?e=m%3D2%26s%3DD5dGgd8bT25w4vFB6t2Z2iperVdZeJvif3ovRFFLMflyINtkUhsv0LnWnKbpSZF5jwT44o8Tf6Q1kicPeK1VfNjcxFgfK5XAhiGWfQvWc46uGOCInnh7loqjIreHZUHg4GfJKEjEJwJzpYkv2aBXViXzcHOJQm%2FHpDKCesgY1gXkwRZR8lHBs2sswmt1oPC%2FA8hgolRGHkczuTGl041QAqC1%2Fwjn0aaPtY4Qt2cZ1lXd4efXitbU8JFcSFnFSJXmsFMnFeqO8gZ5yNE9MYfEdhbJpX7Mxr0b1lzoPAOG4AQEimWme%2FPK7hoyN1WIKpbdxg5p7bh%2BFbQ%3D&union_lens=lensId%3APUB%401603091652%400b521d61_1428_1753fb5614c_398a%4001&direct_sale=1'
# print(parse.unquote(jsRet))  # 输出：中国

tbopen = "tbopen://m.taobao.com/tbopen/index.html?action=ali.open.nav&module=h5&h5Url="

print(parse.quote(jsRet))  # 输出：True

print(parse.quote(jsRet, safe='%'))  # 输出：True