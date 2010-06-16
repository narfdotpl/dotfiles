#!/usr/bin/env ruby

require 'irb/completion'
require 'irb/ext/save-history'


IRB.conf[:PROMPT_MODE] = :SIMPLE
IRB.conf[:AUTO_INDENT] = true
IRB.conf[:HISTORY_FILE] = "#{ENV['HOME']}/.irb_history"
IRB.conf[:SAVE_HISTORY] = 100


def clear
  system 'clear'
end

alias cl clear
