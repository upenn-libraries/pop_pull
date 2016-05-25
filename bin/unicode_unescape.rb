#!/usr/bin/env ruby

IO.foreach(ARGV[0]) do |line|
  puts line.chomp.gsub(/\\u([\da-fA-F]{4})/) {|m| [$1].pack("H*").unpack("n*").pack("U*")}
end
