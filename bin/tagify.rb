#!/usr/bin/env ruby

require 'csv'
require 'set'
require 'unicode'

flickr_tags = Set.new
tag_source = File.expand_path('../../data/tags_from_flickr.csv', __FILE__)
CSV.foreach(tag_source) do |row|
  flickr_tags.add row[0]
end

source_file = File.expand_path('../../data/Tags_Categorized_by_Laura.tsv', __FILE__)

outfile = File.expand_path('../../data/updated_tags.csv',__FILE__)
CSV.open(outfile, 'w+') do |csv|
  CSV.foreach(source_file, col_sep: "\t") do |row|
    text, raw, mitch, laura, model, field, basis = row
    default = 'NO_MATCH'
    if text.nil? || text.strip() == ''
      tag = Unicode::normalize_C(raw.downcase).gsub(/[^[:word:]_]/,'')
      row[0] = flickr_tags.include?(tag) ? tag : "NEW:NO_MATCH:#{tag}"
    else
      flickr_tags.include?(text) or row[0] = "CURR:NO_MATCH:#{tag}"
    end
    csv << row
  end
end

puts "Wrote: #{outfile}"
