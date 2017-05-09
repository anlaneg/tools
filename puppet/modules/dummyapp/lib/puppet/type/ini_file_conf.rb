Puppet::Type.newtype(:ini_file_conf) do
  newparam(:path,:namevar=>true) do
    desc "ini file path"
    newvalues(/^\S+$/)
  end
  newparam(:color) do
    
  end
end