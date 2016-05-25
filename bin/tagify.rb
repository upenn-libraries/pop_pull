#!/usr/bin/env ruby

require 'csv'
require 'set'
require 'unicode'

flickr_tags = Set.new
tag_source = File.expand_path('../../data/tags_from_flickr.csv', __FILE__)
CSV.foreach(tag_source) do |row|
  flickr_tags.add row[0]
end

source_file = File.expand_path('../../data/POPTagList_Mitch_and_Laura_Categories_Sheet1.csv', __FILE__)

outfile = File.expand_path('../../data/updated_tags.csv',__FILE__)
CSV.open(outfile, 'w+') do |csv|
  CSV.foreach(source_file) do |row|
    text, raw, mitch, laura, model, field, basis = row
    default = 'NO_MATCH'
    if text.nil? || text.strip() == ''
      tag = Unicode::normalize_C(raw.downcase).gsub(/[^[:word:]_]/,'')
      row[0] = flickr_tags.include?(tag) ? tag : "NEW:NO_MATCH:#{tag}"
    else
      if ! flickr_tags.include? text
        row[0] =  "CURR:NO_MATCH:#{text}"
      end
    end
    csv << row
  end
end

puts "Wrote: #{outfile}"
