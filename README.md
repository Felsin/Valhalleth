# Valhall.eth
This is a Python script to autorefresh IPFS/IPFN hosted ENS site with a dynamic website showing a progress counter for Eth price reaching $10,000

Visit Valhall.eth.link for an example.

This site requires a index.html, styles.css, ipfs_hashes.txt, ipfn_hashes.txt, pinata_hashes.txt, script_log.txt, whatever images or robot.txt you include, and the script itself. 

ipfs_hashes.txt, pinata_hashes.txt and ipfn_hashes.txt need atleast one character in them the first time the script is ran since it attempts to remove the old pinned data. Any empty lines at the bottom of these files will also cause errors (just a newbie here..improvements welcomed!)

The structure of the index.html must have the data for your base content section on their own separate line with no formatting before or after the text. The script must be adapted to match the data in your file.

This data from the index.html must be on its own line and the script must be adapted to any changes made to this main content section:

"ETH Price / $10,000 
Progress:
[############----------------------------------------------------------------------------------------]12% 
Current Price: $1222.66 
Last Updated: 2021-01-22 19:01:51.008584
Highest Price Achieved: $1438.12"
  
You must enter missing variables into the script including your twitter API keys, pinata API keys, and coingecko API keys.

Have fun learning!
@felblob




