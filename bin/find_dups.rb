require 'csv'


tags = {}
text = []
rows = CSV.new(File.open(File.expand_path('../../output/all_tags.csv', __FILE__))).read

rows.each do |row|
  (tags[row[0]] ||= []) << row
  text << row[0]
end

last = nil
text.sort!
dups = []
text.each do |t|
  if t == last
    dups << t unless dups.include?(t)
    last = nil
  else
    last = t
  end
end

CSV.open('x.csv', 'wb') do |csv|
  dups.each do |dup|
    tags[dup].each { |t| csv << t }
  end
end
