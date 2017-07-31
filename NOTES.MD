# Emoji
Emojis are not images, they are nodes with custom styles that set their background. The background's link looks like this: `/images/emoji.php/$VERSION/$ID` where `$VERSION` is `v9` for me.

# (known) Errors
Since I can't produce server-side errors on my own, I have to rely on manual testing. So far I know of two errors:
## Skipping
Going back in the thread can sometimes skip a message, afaik it is related to whether there is a link preview or image around, going back and forth seems to fix it, needs more investigation.
## Fails to open conversation
Sometimes facebook just flat out refuses to open something and throws you to an error page. The URL is the same and afaik there is no HTTP code indicating it. I was "lucky" enough to encounter it and there seems to be a simple DOM query to check if we are on that page. There is no known workaround besides waiting until they fix their shit.

# Handling errors (TODO)
Failed downloads should go into a/multiple queue(s), that's for sure, what's not is how to save state to disk efficiently and 100% safely. There should probably be an external `try/catch` that saves progress no matter what happens and also some periodic writing, either done by checking the time or done at every `N` pages.
