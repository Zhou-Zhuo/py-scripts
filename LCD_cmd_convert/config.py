inListPrefixPattern = r'qcom,mdss-dsi-on-command = \['
inListSuffixPattern = r'\];'
inCmdPrefixPattern = r'39 01 00 00 00 00'
outCmdPrefixFormat = 'static char panel_cmd_array%d[] = {\n'
outCmdMagic = '00 39 C0'
outCmdSuffix = '\n};\n'
