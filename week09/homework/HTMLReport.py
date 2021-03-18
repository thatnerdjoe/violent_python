'''
Asset Map Report Module
Professor Hosmer
October 2020
'''
# HTML REPORT TEMPLATE

HTML_START = '''
<html>
<head>
	<title>Python Passive Asset Mapping .99-1 Experimental Results</title>
</head>
<body style="cursor: auto;">
<p><span style="color:#B22222;"><span style="font-size:36px;"><span style="font-family:tahoma,geneva,sans-serif;"><strong>Python Asset Map<strong></span></span></span></p>

<p><u><span style="color:#808080;"><span style="font-size:24px;"><font face="tahoma, geneva, sans-serif"><b>Overview</b></font></span></span></u></p>

<table border="4" cellpadding="3" cellspacing="2" style="width: 832px;">
	<thead>
	</thead>
	<tbody>
		<tr>
			<td style="width: 249px;"><strong>Script Name</strong></td>
			<td style="width: 553px;">{fldScriptName}</td>
		</tr>
		<tr>
			<td style="width: 249px;"><strong>Script Author</strong></td>
			<td style="width: 553px;">{fldAuthor}</td>
		</tr>
		<tr>
			<td style="width: 249px;"><strong>Script Version</strong></td>
			<td style="width: 553px;">{fldVersion}</td>
		</tr>
		<tr>
			<td style="width: 249px;"><strong>Target File</strong></td>
			<td style="width: 553px;">{fldTarget}</td>
		</tr>
        
        <tr>
			<td style="width: 249px;"><strong>Report File</strong></td>
			<td style="width: 553px;">{fldReportFile}</td>
		</tr>
        
        <tr>
			<td style="width: 249px;"><strong>Analyst</strong></td>
			<td style="width: 553px;">{fldAnalyst}</td>
		</tr>
        
        <tr>
			<td style="width: 249px;"><strong>Organization</strong></td>
			<td style="width: 553px;">{fldOrg}</td>
		</tr>
        
        <tr>
			<td style="width: 249px;"><strong>Baseline Description</strong></td>
			<td style="width: 553px;">{fldBaseline}</td>
		</tr>
        
		<tr>
			<td style="width: 249px;">&nbsp;</td>
			<td style="width: 553px;">&nbsp;</td>
		</tr>
		<tr>
			<td style="width: 249px;"><strong>Scan Start</strong></td>
			<td style="width: 553px;">{fldStart}</td>
		</tr>
		<tr>
			<td style="width: 249px;"><strong>Scan End</strong></td>
			<td style="width: 553px;">{fldEnd}</td>
		</tr>
        
        <tr>
			<td style="width: 249px;"><strong>Packets Processed</strong></td>
			<td style="width: 553px;">{fldPkts}</td>
		</tr>

	</tbody>
</table>

'''
HTML_SECTION = '''
<body>
<p>
<hr>
<p><u><span style="color:#808080;"><span style="font-size:24px;"><font face="tahoma, geneva, sans-serif"><b>Unique Observations</b></font></span></span></u></p>

<table border="3" bordercolor="black" bgcolor="LemonChiffon" style="text-align: left;">

<thead>
<tr>
<td colspan="10"><h3>Python Asset Mapping Results</h3></td>
<td colspan="24"><h3>......Hourly-Occurrences..... </h3></td>
</tr>
</thead>
<tfoot>
<tr>
<td colspan="9">CYBV-473 - Your Name</td>
</tr>
</tfoot>
<tr>
<th>SRC IP</th>
<th>DST IP</th>
<th>SrcPort</th>
<th>DstPort</th>
<th>Type</th>
<th>SrcMAC</th>
<th>DstMAC</th>
<th>SrcMFG</th>
<th>DstMFG</th>
<th>..</th>
<th>HR-00</th>
<th>HR-01</th>
<th>HR-02</th>
<th>HR-03</th>
<th>HR-04</th>
<th>HR-05</th>
<th>HR-06</th>
<th>HR-07</th>
<th>HR-08</th>
<th>HR-09</th>
<th>HR-10</th>
<th>HR-11</th>
<th>HR-12</th>
<th>HR-13</th>
<th>HR-14</th>
<th>HR-15</th>
<th>HR-16</th>
<th>HR-17</th>
<th>HR-18</th>
<th>HR-19</th>
<th>HR-20</th>
<th>HR-21</th>
<th>HR-22</th>
<th>HR-23</th>
</tr>
'''

HTML_ENTRY = '''

<tr>
<td>{fldSrcIP}</td>
<td>{fldDstIP}</td>
<td>{fldSrcPort}</td>
<td>{fldDstPort}</td>
<td>{fldType}</td>
<td>{fldSrcMAC}</td>
<td>{fldDstMAC}</td>
<td>{fldSrcMFG}</td>
<td>{fldDstMFG}</td>
<td>  </td>
<td>{fldHr[0]}</td>
<td>{fldHr[1]}</td>
<td>{fldHr[2]}</td>
<td>{fldHr[3]}</td>
<td>{fldHr[4]}</td>
<td>{fldHr[5]}</td>
<td>{fldHr[6]}</td>
<td>{fldHr[7]}</td>
<td>{fldHr[8]}</td>
<td>{fldHr[9]}</td>
<td>{fldHr[10]}</td>
<td>{fldHr[11]}</td>
<td>{fldHr[12]}</td>
<td>{fldHr[13]}</td>
<td>{fldHr[14]}</td>
<td>{fldHr[15]}</td>
<td>{fldHr[16]}</td>
<td>{fldHr[17]}</td>
<td>{fldHr[18]}</td>
<td>{fldHr[19]}</td>
<td>{fldHr[20]}</td>
<td>{fldHr[21]}</td>
<td>{fldHr[22]}</td>
<td>{fldHr[23]}</td>
</tr>

'''

HTML_TABLE_END = '''
</table>
'''

HTML_PORTS = '''

<body>
<p>
<hr>
<p><u><span style="color:#808080;"><span style="font-size:24px;"><font face="tahoma, geneva, sans-serif"><b>Server Port Usage Observations</b></font></span></span></u></p>

<table border="3" bordercolor="black" bgcolor="LemonChiffon" style="text-align: left;">

<thead>
<tr>
<td colspan="3"><h3>Python Port Usage Map</h3></td>
</tr>
</thead>
<tfoot>
<tr>
<td colspan="6">CYBV-473: Your Name</td>
</tr>
</tfoot>
<tr>
<th><b>IP</b></th>
<th><b>Port</b></th>
<th><b>Description</b></th>
'''

HTML_ENTRY_PORTS = '''
<tr>
<td>{fldPortIP}</td>
<td>{fldPortNum}</td>
<td>{fldPortDesc}</td>
</tr>
'''

HTML_END = '''
<p>&nbsp;</p>
</body>

</html>
'''