# py-pastebin
Command line utility to create new pastes on pastebin.com.

## Usage
### Login to pasebin account
```
py-pastebin.py --login -u <USER> -p <PASSWORD> -d <API DEV KEY>
```
### New paste, conetent passed as option
```
py-pastebin.py -c "This is my content."
```
### New paste, conetent read from file
```
py-pastebin.py -f /etc/fstab
```
### New paste, conetent read from standard input
```
cat /etc/hosts | py-pastebin.py -s
```
