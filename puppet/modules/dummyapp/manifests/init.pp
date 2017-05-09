
class dummyapp()
{
	  resources { 'ini_file_conf':
    purge => true,
  }
	ini_file_conf{'myini_file':
		#path => '/usr/lib/an.txt',
		'abc': value => 'abc',
	}
}