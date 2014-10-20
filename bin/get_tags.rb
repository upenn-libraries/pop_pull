require 'json'
require 'csv'

data_dir = File.expand_path('../../data', __FILE__)
json_files = Dir[data_dir + '/POP_*.json']


puts json_files

tags = {}

json_files.each do |f|
  records = JSON.parse(IO.read(f))
  records.each do |rec|
    rec['photo']['tags']['tag'].each do |tag|
      raw = tag['raw']
      tags[raw] ||= tag
    end
  end
end

CSV.open("all_tags_ruby.csv", "wb") do |csv|
  csv << %w( text raw author )
  tags.each do |raw, tag|
    csv << [ tag['text'], raw, tag['authorname'] ]
  end
end
