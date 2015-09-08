#!/usr/bin/perl 
# Author Martin Leucht 2015 <martin.leucht@os3.nl>
#
# Benchmarking tool for HTTP/2 servers/reverse proxies
# based on h2load nghttp2/0.7.6-DEV 
# https://nghttp2.org/documentation/h2load.1.html
#
# If used against an HTTP/2 reverse proxy that translates/forwards
# requests to an HTTP/1.1 server, this tool can also measure
# the performance of HTTP/1.1 enabled servers.
#
# Usage: ./measure.pl [URL-list-file]
#
# Output is written to an CSV file

use List::Util qw(sum);
use strict;
use warnings;

my $file_urls = $ARGV[0];

my $runs=20;
my $stepsize_requests=10;
my $stepsize_clients=5;
my $parallel_clients = 50;
my $number_of_requests = 1000;

my $bin_v2 = '/usr/local/bin/h2load';


sub check{
	my %units = ('1000' => 's','0.001' => 'us','1' => 'ms',);
	my $value = shift;
	my $unit = shift;
	
	foreach my $key (keys %units) {
		if ($units{$key} eq $unit) {
			our $ret = $key * $value;
			}
		}		
return our $ret;
}


for (my $n=10; $n <= $parallel_clients; $n=$n+$stepsize_clients) {  

	my $time = time;
	my $filename = "report_http_${file_urls}_clients_${n}_${time}.csv";
	open(my $fh, '>', $filename) or die "Could not open file '$filename' $!";
	print $fh "number_of_requests,total_time_test,req_per_sec_v2,speed,traffic_total,traffic_header,traffic_data,min_request,max_request,mean_request,sd_request,sd_percent_request,succeeded_requests,succeeded_failed\n";
	close $fh;

	for (my $j=$n; $j <= $number_of_requests; $j=$j+$stepsize_requests) {

		print "\n\nnumber_of_requests $j number of clients $n number of runs $runs\n\n";

		my @finished_total_time_v2= ();
                my @finished_req_per_sec_v2 = ();
                my @finished_speed_v2 = ();
                my @finished_traffic_total_v2= ();
                my @finished_traffic_header_v2 = ();
                my @finished_traffic_data_v2 =();
                my @finished_min_request_v2 =();
                my @finished_max_request_v2 =();
                my @finished_mean_request_v2 =();
                my @finished_sd_request_v2 =();
                my @finished_sd_percent_request_v2 =();
                my @finished_succeeded =();
                my @finished_failed =();



		for (my $i=1; $i <= $runs; $i++) {


		
			my @command = `$bin_v2 -n $j -c $n --input-file=$file_urls --max-concurrent-streams=auto`;
#			print "@command \n";						
	
			foreach my $line (@command) {

				if ( $line =~ m/^finished.*?([0-9]*\.[0-9]*)(\w{1,2}).*?(\d+)\s.*?(\d+\.\d+).*/ ) {
				
					my $val = check($1,$2);	
					push(@finished_total_time_v2, $val);
					push(@finished_req_per_sec_v2, $3);
					push(@finished_speed_v2, $4);
					}
				elsif ( $line =~ m/^traffic.*?(\d+).*?(\d+).*?(\d+).*/ ) {	
					push(@finished_traffic_total_v2, $1);
                			push(@finished_traffic_header_v2, $2);
                			push(@finished_traffic_data_v2, $3);
					}
				
				 elsif ( $line =~ m/^requests.*?(\d+)\s(?=succeeded).*?(\d+)\s(?=failed)/ ) {
					push(@finished_succeeded, $1);
					push(@finished_failed, $2);
					}	
					
				elsif ( $line =~ m/^time.*?(\d+\.*\d*)(\w{1,2}).*?(\d+\.*\d*)(\w{1,2}).*?(\d+\.*\d*)(\w{1,2}).*?(\d+\.*\d*)(\w{1,2}).*?(\d+\.*\d*).*/ ) {
					#print "############ $line \n";
					my $val1 = check($1,$2);
					my $val2 = check($3,$4);
					my $val3 = check($5,$6);
					my $val4 = check($7,$8);

                			push(@finished_min_request_v2, $val1);
					push(@finished_max_request_v2, $val2);
					push(@finished_mean_request_v2, $val3);
					push(@finished_sd_request_v2, $val4);
					push(@finished_sd_percent_request_v2, $9);
					}
				else {print "";}
			}
		}	


		my $mean_finished_total_time_v2 = sprintf("%.6f", average(@finished_total_time_v2));
		my $mean_finished_req_per_sec_v2 = sprintf("%.2f",average(@finished_req_per_sec_v2));
		my $mean_finished_speed_v2 = sprintf("%.2f",average(@finished_speed_v2));
		my $mean_finished_traffic_total_v2 = sprintf("%.0f",average(@finished_traffic_total_v2));
		my $mean_finished_traffic_header_v2 = sprintf("%.0f",average(@finished_traffic_header_v2));
		my $mean_finished_traffic_data_v2 = sprintf("%.0f",average(@finished_traffic_data_v2));
		my $mean_finished_min_request_v2 = sprintf("%.6f",average(@finished_min_request_v2));
		my $mean_finished_max_request_v2 = sprintf("%.6f",average(@finished_max_request_v2));
		my $mean_finished_mean_request_v2 = sprintf("%.6f",average(@finished_mean_request_v2));
		my $mean_finished_sd_request_v2 = sprintf("%.6f",average(@finished_sd_request_v2));
		my $mean_finished_sd_percent_request_v2 = sprintf("%.2f",average(@finished_sd_percent_request_v2));
		my $mean_finished_succeeded_v2 = sprintf("%.0f",average(@finished_succeeded));
		my $mean_finished_failed_v2 = sprintf("%.0f",average(@finished_failed));
	
		print "Mean finished total time: $mean_finished_total_time_v2 ms\n";
		print "mean_finished_req_per_sec_v2: $mean_finished_req_per_sec_v2 req/s\n";
		print "mean_finished_speed_v2: $mean_finished_speed_v2 MB/s\n";
		print "mean_finished_traffic_total_v2: $mean_finished_traffic_total_v2 byte\n";
		print "mean_finished_traffic_header_v2: $mean_finished_traffic_header_v2 byte\n";
		print "mean_finished_traffic_data_v2: $mean_finished_traffic_data_v2 byte\n";
		print "mean_finished_min_request_v2: $mean_finished_min_request_v2 ms\n";
		print "mean_finished_max_request_v2: $mean_finished_max_request_v2 ms \n";
		print "mean_finished_mean_request_v2: $mean_finished_mean_request_v2 ms\n";
		print "mean_finished_sd_request_v2: $mean_finished_sd_request_v2 ms\n";
		print "mean_finished_sd_percent_request_v2: $mean_finished_sd_percent_request_v2 %\n";
		print "mean_finished_succeeded: $mean_finished_succeeded_v2\n";
                print "mean_finished_failed_v2: $mean_finished_failed_v2\n";


        	open(my $fh, '>>', $filename) or die "Could not open file '$filename' $!";
        	print $fh "$j,$mean_finished_total_time_v2,$mean_finished_req_per_sec_v2,$mean_finished_speed_v2,$mean_finished_traffic_total_v2,$mean_finished_traffic_header_v2,$mean_finished_traffic_data_v2,$mean_finished_min_request_v2,$mean_finished_max_request_v2,$mean_finished_mean_request_v2,$mean_finished_sd_request_v2,$mean_finished_sd_percent_request_v2,$mean_finished_succeeded_v2,$mean_finished_failed_v2\n";
        	close $fh;
		
	}			

}

sub average {
	my $size = @_;
	
	if ($size == 0) {
		print "NA";
		}
	else {return sum(@_)/@_;}
}


