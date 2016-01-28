@echo off
cd files
qemu -L . -m 128 -hda ReactOS.vmdk -net nic,model=ne2k_pci -net user -cdrom ReactOS.iso -boot d
