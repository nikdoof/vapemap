Vagrant::Config.run do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  config.vm.host_name = "vapemap.local"
  config.vm.forward_port 80, 8080

  config.vm.provision :shell, :inline => "apt-get update --fix-missing"
  config.vm.provision :puppet do |puppet|
      puppet.manifests_path = "puppet/manifests"
      puppet.manifest_file  = "vagrant.pp"
      puppet.options = ['--templatedir', '/vagrant/puppet/templates']
  end
end
