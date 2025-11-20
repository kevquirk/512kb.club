require 'yaml'
require 'rexml/document'
require 'date'
require 'time'
include REXML

module RSSGenerator
  class Generator < Jekyll::Generator
    def generate(site)
      # Read the YAML file
      websites = YAML.load_file(
        File.join(site.source, '_data', 'sites.yml'),
        permitted_classes: [Date]
      )

      # Ensure we always sort comparable values
      websites.each do |website|
        raw_date = website['last_checked']
        website['last_checked'] =
          case raw_date
          when Time
            raw_date
          when Date, DateTime
            raw_date.to_time
          when String
            begin
              Time.parse(raw_date)
            rescue ArgumentError
              nil
            end
          else
            nil
          end
      end

      # Sort websites by "last_checked" in descending order
      websites.sort_by! { |website| website['last_checked'] || Time.at(0) }.reverse!

      # Get the 10 latest entries
      latest_websites = websites.take(10)

      # Create the RSS feed XML
      rss = Element.new('rss')
      rss.add_attribute('version', '2.0')

      channel = Element.new('channel')
      rss.add_element(channel)

      title = Element.new('title')
      title.text = '512KB Club'
      channel.add_element(title)

      link = Element.new('link')
      link.text = 'https://512kb.club'
      channel.add_element(link)

      description = Element.new('description')
      description.text = 'Updates for the 512KB Club.'
      channel.add_element(description)

      latest_websites.each do |website|
        item = Element.new('item')
        channel.add_element(item)

        title = Element.new('title')
        title.text = "512KB Club: #{website['domain']} was added or updated"
        item.add_element(title)

        link = Element.new('link')
        link.text = website['url']
        item.add_element(link)

        pub_date = Element.new('pubDate')
        pub_time = website['last_checked'] || Time.now
        pub_date.text = pub_time.strftime('%a, %d %b %Y %H:%M:%S %z')
        item.add_element(pub_date)

        description = Element.new('description')
        description.text = "#{website['domain']} was added to the 512KB Club, or the entry was updated. Size: #{website['size']}"
        item.add_element(description)
      end

      FileUtils.mkdir_p(site.dest) unless File.exist?(site.dest)
      formatter = REXML::Formatters::Pretty.new
      formatter.compact = true

      # Write the RSS feed XML to a file
      rss_file_path = File.join(site.dest, 'feed.xml')
      File.open(rss_file_path, 'w') do |file|
        formatter.write(rss.root, file)
      end

      Jekyll::StaticFile.new(site, site.dest, '/', 'feed.xml')
      site.keep_files << "feed.xml"
    end
  end
end
