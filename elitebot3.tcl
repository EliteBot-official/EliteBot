#!/usr/bin/tclsh
 
# Bot Settings
BNICK   = 'EliteBot'
BIDENT  = 'EliteBot'
BNAME   = 'EliteBot'
BALT    = 'EliteBot-'
BHOME   = '#EliteBot'

# Connection Settings
BPORT   =  '+6697'
BSERVER = 'irc.technet.chat'
 
# SASL Configuration.
UseSASL = True
SANICK  = 'EliteBot'
SAPASS  = 'password'

proc ircsplit str {
	set res {}
	if {[string index $str 0] eq ":"} {
		lappend res [string range $str 1 [set first [string first " " $str]]-1]
		set str [string range $str 1+$first end]
	} else {
		lappend res {}
	}
	if {[set pos [string first " :" $str]] != -1} {
		lappend res {*}[split [string range $str 0 ${pos}-1]]
		lappend res [string range $str 2+$pos end]
	} else {
		lappend res {*}[split $str]
	}
	return $res
}
set sockChan [socket $::server $::port]
fconfigure $sockChan -translation crlf -buffering line
puts $sockChan "NICK $::botnick"
puts $sockChan "USER $::realname * * :$::ident"
while {![eof $sockChan]} {
	set line [gets $sockChan]
	puts ">> $line"
	set lline [ircsplit $line]
	set chan [lindex $lline 2]
	set text [lindex $lline end]
	switch -nocase -- [lindex $lline 1] {
		PING {puts $sockChan "PONG :[lindex $lline 2]"}
		001 {puts $sockChan "JOIN #test"}
		PRIVMSG {switch -- [lindex $lline 3] {
				!quit {
					puts $sockChan "QUIT :Requested"
					close $sockChan
					return
				}
			}
		}
	}
}
