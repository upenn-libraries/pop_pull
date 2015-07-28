#!/usr/bin/env ruby

require 'json'
require 'set'
require 'pp'
require 'axlsx'

data_dir = File.expand_path '../../data', __FILE__
outfile = 'photos.xlsx'

class Book
  attr_accessor :line, :parts, :props

  NORMAL_RE  = /\W/
  FOLIO_RE   = /^Folio\s*/i

  NAMES = %w(
    call bibid title author conference pub date provenance printplace
  ).map(&:to_sym)

  class << self
    def normalize s
      s and s.strip.gsub(/\W/,'').downcase
    end
  end

  def initialize line
    @line = line.chomp
    @parts = line.split(/\t/)
    @props = {}
    # call, bibid, title, author, conference, pub, date, provenance, printplace
    NAMES.each_with_index do |name,index|
      @props[name] = @parts[index]
    end
  end

  def callno
    if props[:call] =~ FOLIO_RE
      "#{$'} folio"
    else
      props[:call]
    end
  end

  def bibid
    props[:bibid]
  end

  def normal_callno
    Book.normalize callno
  end
end

class Books
  attr_accessor :tsv_file

  def initialize tsv_file
    @tsv_file = tsv_file
    @call_to_bibid = {}
    @books = []
    @callno_map = {}
    @index = 0
    load_tsv
  end

  def load_tsv
    IO.readlines(tsv_file).drop(1).each do |line|
      book = Book.new line
      @books << book
      @callno_map[book.normal_callno] = book
    end
  end

  def each
    return enum_for(:each) unless block_given?

    @books.each do |book|
      yield book
    end
  end

  def find callno
    @callno_map[Book.normalize callno]
  end
end

class Categories
  attr_accessor :csv, :cat_set, :tags, :cats
  NOT_FOUND = %w( NOT_FOUND NOT_FOUND )

  def initialize csv
    @csv = csv
    @cat_set = Set.new
    @tags = {}
    @cats = []
    load_csv
  end

  def load_csv
    IO.foreach csv do |line|
      ugly, raw, mitch, laura, model, field = line.chomp.split "\t"
      cat = [ model.strip.downcase, field.strip.downcase ]
      tags[raw.strip.downcase] = cat
      cat_set.add cat
      cat_set.add(cat)
    end
    @cats = cat_set.to_a
    @cats.sort!
  end
end # class Categories

class Photo
  attr_accessor :record, :tag_hash

  def initialize record, categories
    @record = record
    @tag_hash = {}
    map_tags categories
end

  def photo
    record['photo']
  end

  def photo_id
    photo['id']
  end

  def title
    photo['title']
  end

  def url
    photo['urls']['url'].first['text']
  end

  def tags
    photo['tags']['tag']
  end

  def all_tag_vals key
    tags.map { |t| t[key] }
  end

  def raw_tags
    all_tag_vals 'raw'
  end

  def text_tags
    all_tag_vals 'text'
  end

  def map_tags categories
    (@tag_map ||= {})[Categories::NOT_FOUND] = []
    raw_tags.each do |tag|
      cat = categories.tags[tag.strip.downcase] || Categories::NOT_FOUND
      if cat == Categories::NOT_FOUND
        $stderr.puts "Tag not found: #{tag}; photo_id: #{photo_id}"
      end
      (@tag_map[cat] ||= []) << tag
    end
  end

  def mapped_tags
    @tag_map || {}
  end

  def call_nos
    mapped_tags[['copy','call number']] || []
  end

  def tags_for category
    mapped_tags[category] || []
  end
end

cats = Categories.new ARGV.shift

books = Books.new File.join data_dir, 'call_bidid_map.tsv'

head = %w{ ID Title URL BibID }
cats.cats.reduce(head) { |a,c| a << c.join(':'); a }

p = Axlsx::Package.new
wb = p.workbook
wb.add_worksheet name: 'photos' do |wksh|
  wksh.add_row head
  Dir[File.join data_dir, 'NFC', '*.json'].each do |file|
    records = JSON.load(File.open(file))
    records.each_with_index do |record,index|
      photo = Photo.new record, cats
      row = [ photo.photo_id, photo.title, photo.url ]
      # tags = photo.mapped_tags
      bibids = photo.call_nos.flat_map { |call|
        book = books.find call
        book ? [ book.bibid ] : []
      }
      row << bibids.join('|')
      cats.cats.each do |cat|
        row << photo.tags_for(cat).join('|')
      end
      row = row.map { |x| x == '' ? nil : x }
      wksh.add_row row
    end

    wksh.column_widths(*Array.new(head.size, 20))
  end
end

p.serialize outfile
puts "Wrote '#{outfile}'"
