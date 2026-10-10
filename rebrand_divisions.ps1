$f = "c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Test\Web\index.html"
$c = [System.IO.File]::ReadAllText($f, [System.Text.Encoding]::UTF8)

# Meta description
$c = [regex]::Replace($c, 'content="Royalty Executive Empire Limited \(REEL\) is a premium holding company delivering mobile charging infrastructure.*?across Africa\."',
    'content="Royalty Executive Empire Limited (REEL) is a premium holding company with four core divisions &mdash; REEL Tech Hub, REEL Auto Centre, REEL Properties, and REEL Global Palace &mdash; Building Empires, Shaping Futures, and Leading Innovation across Africa and the world."')

# Meta keywords - old ones
$c = [regex]::Replace($c, 'content="REEL, Royalty Executive Empire Limited, REEL Power, REEL Branding, REEL Properties[^"]*"',
    'content="REEL, Royalty Executive Empire Limited, REEL Tech Hub, REEL Auto Centre, REEL Properties, REEL Global Palace, executive infrastructure Africa, technology hub Nigeria, auto centre Lagos, real estate Africa, luxury lifestyle"')

# JSON-LD subOrganization
$c = [regex]::Replace($c, '(?s)"subOrganization": \[.*?\],',
    '"subOrganization": [' + "`r`n" +
    '      { "@type": "Organization", "name": "REEL Tech Hub" },' + "`r`n" +
    '      { "@type": "Organization", "name": "REEL Auto Centre" },' + "`r`n" +
    '      { "@type": "Organization", "name": "REEL Properties" },' + "`r`n" +
    '      { "@type": "Organization", "name": "REEL Global Palace" }' + "`r`n" +
    '    ],')

# Mission text
$c = [regex]::Replace($c, 'power, branding, property, and growth &mdash; that enables Africa&rsquo;s leaders and enterprises to operate without compromise\.',
    'technology, automotive, property, and lifestyle &mdash; that enables Africa&rsquo;s leaders and enterprises to operate without compromise.')

# Capabilities card heading and text
$c = $c.Replace('One Partner, Four Capabilities', 'One Partner, Four Divisions')
$c = [regex]::Replace($c, 'Power, branding, property, and growth strategy &mdash; under a single trusted relationship, so enterprise clients can consolidate vendors without compromising on quality\.',
    'Technology, automotive, property, and lifestyle &mdash; under a single trusted REEL relationship, so clients can access premium excellence across every need without compromise.')

[System.IO.File]::WriteAllText($f, $c, [System.Text.Encoding]::UTF8)
Write-Host "Done - all meta, schema and text updates applied."
