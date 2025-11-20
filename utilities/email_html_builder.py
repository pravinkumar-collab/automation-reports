def build_email_body(total, passed, failed, skipped, report_time, zip_password="FatakPay123"):

    html = (
        '<table width="600" align="center" cellpadding="0" cellspacing="0" '
        'style="margin:0 auto;padding:0;border-collapse:collapse;font-family:Arial,Helvetica,sans-serif;">'

        '<tr><td style="padding:0;margin:0;font-size:20px;font-weight:bold;color:#2e6c80;text-align:center;">'
        'Automation Test Report'
        '</td></tr>'

        '<tr><td style="padding:10px 0 0 0;margin:0;font-size:13px;color:#333;">'
        'Hello Team,'
        '</td></tr>'

        '<tr><td style="padding:10px 0 0 0;margin:0;font-size:13px;color:#333;">'
        'The automated test suite for <b>Insurance (Web)</b> has completed.<br>'
        'Please find the summary below:'
        '</td></tr>'

        '<tr><td style="padding:10px 0;margin:0;">'
        '<table width="100%" cellpadding="4" cellspacing="0" '
        'style="border-collapse:collapse;margin:0;padding:0;text-align:center;font-size:12px;">'

        '<tr style="background:#f0f0f0;font-weight:bold;">'
        '<td style="border:1px solid #ccc;">Total</td>'
        '<td style="border:1px solid #ccc;">Passed</td>'
        '<td style="border:1px solid #ccc;">Failed</td>'
        '<td style="border:1px solid #ccc;">Skipped</td>'
        '<td style="border:1px solid #ccc;">Time (s)</td>'
        '</tr>'

        f'<tr>'
        f'<td style="border:1px solid #ccc;">{total}</td>'
        f'<td style="border:1px solid #ccc;color:green;font-weight:bold;">{passed}</td>'
        f'<td style="border:1px solid #ccc;color:red;font-weight:bold;">{failed}</td>'
        f'<td style="border:1px solid #ccc;">{skipped}</td>'
        f'<td style="border:1px solid #ccc;">{report_time}</td>'
        '</tr>'

        '</table>'
        '</td></tr>'

        # ⭐ ADDED PASSWORD SECTION (NON-BREAKING)
        f'<tr><td style="padding:10px 0 0 0;margin:0;font-size:13px;color:#333;">'
        f'<b>ZIP Password:</b> <span style="color:#d9534f;">{zip_password}</span>'
        '</td></tr>'

        '<tr><td style="padding:10px 0;margin:0;font-size:13px;color:#333;">'
        'The complete Allure report is attached as a password-protected ZIP file.<br>'
        'Unzip and open <b>index.html</b> to view the full report.'
        '</td></tr>'

        '<tr><td style="padding:10px 0;margin:0;font-size:13px;color:#333;">'
        'Regards,<br>'
        '<b>An SDET from the QA Automation Team.</b><br>'
        'FatakPay'
        '</td></tr>'

        '</table>'
    )
    return html
