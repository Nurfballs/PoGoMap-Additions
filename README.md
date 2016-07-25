# PoGoMap-Additions
When used in conjunction with the gps module, will send a pushover notification of nearby pokemon with a link to directions via google maps.

# Instructions
Create a /config/pushoverconfig.json file.

##Parameters:
* "notify" - comma separated list of pokemon you want to be notified about.
* "token" - your pushover application token.
* "user" - your pushover user key

```Example:
{
  "notify"			: "zubat",
	"token"				: "123456",
	"user"				: "123456"
}
```
