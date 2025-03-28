from backend.emails.email_service import send_email

html = """
<h2>Hai Sahabat Neutron!</h2>
<p>Ini hanya uji coba pengiriman email.</p>
"""

result = send_email("alamat_emailmu@gmail.com", "Tes Email dari Neutron", html)
print(result)
