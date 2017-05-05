Puppet::Type.newtype(:ini_file_conf) do
  newproperty(:path) do
    desc "ini file path"
    newvalues(/^\S+$/)
  end
  newparam(:key,:keyvar) do
    newvalues(/\S+\/\S+/)
  end
end