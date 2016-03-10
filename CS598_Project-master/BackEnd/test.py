


l = [u',', u'Rape\U0001f616', u'Abuse\U0001f44a', u'Periods\U0001f534', u'Abortion\U0001f637', u'Pregnancy\U0001f476', u'Harassment\U0001f44b', u'Breast', u'cancer\U0001f6ba', u'Being', u'walked', u'on\U0001f45f', u'Being', u'cheated', u'on\U0001f64d', u'Females', u'Do', u'go', u'through', u'a', u'lot', u'\U0001f629\U0001f602']



l= [eliminate_unicode(i) for i in l]
print l


print eliminate_unicode("through\u2026")
