# Runbook: reflash a Jetson to JetPack 7.2.1

Step 1 of `JAZZY_PLAN.md`. Target: Orin Nano Super 8 GB devkit, NVMe,
JetPack 6.2.x / L4T R36.5 to JetPack 7.2.1 / L4T R39.2.1 / kernel 6.8.
Examples use `ts-nano-dev` / `nano-dev`; substitute the board and account
you are flashing. See [hardware status](JAZZY_PLAN.md#hardware-status) for
remaining migration work. Laptop commands run on Arch, board commands on the Jetson.
Budget half a day. You need a DisplayPort monitor and a USB keyboard at the
board (the devkit has no HDMI), a 16 GB+ USB stick and Ethernet.

## 0. Already done on the laptop (2026-09-26)

ISO: `~/Downloads/jetpack-7.2.1/jetsoninstaller-r39.2.1-2026-08-07-18-30-47-arm64.iso`,
5,035,601,920 bytes. SHA-1 `8549f0b3336a9141e035ad3726475190d9766f2f`
matches NVIDIA's `release_sha_hashes.txt` (saved next to it). NVIDIA
publishes only SHA-1. Recheck before writing the stick:

```bash
cd ~/Downloads/jetpack-7.2.1 && sha1sum -c <(grep iso release_sha_hashes.txt)
```

Sources: [JetPack 7.2.1 downloads](https://developer.nvidia.com/embedded/jetpack/downloads/archive-7.2.1),
[hash list](https://developer.nvidia.com/downloads/embedded/L4T/r39_Release_v2.1/release/release_sha_hashes.txt).

## 1. Before flashing

No disk image or file backup is needed for standard: the user confirmed
nothing important remains on it (2026-10-06). Flash it as a clean install.
Models and source come from their repositories; see the
[hardware checklist](JAZZY_PLAN.md#hardware-checklist) for the ONNX source
and TensorRT rebuild. Any Humble performance comparison needs a recorded
baseline; see [hardware status](JAZZY_PLAN.md#hardware-status).

## 2. Write the USB stick (laptop, Arch)

NVIDIA's guide says to use Balena Etcher. The ISO is a hybrid GPT image, so
`dd` writes it the same way.

```bash
lsblk -dpo NAME,SIZE,MODEL,TRAN,RM        # before plugging in the stick
# plug in the stick
lsblk -dpo NAME,SIZE,MODEL,TRAN,RM        # the new line with TRAN=usb, RM=1 is the stick
DEV=/dev/sdX                               # set from the line above; never nvme0n1
udisksctl unmount -b ${DEV}1 2>/dev/null; udisksctl unmount -b ${DEV}2 2>/dev/null
ISO=~/Downloads/jetpack-7.2.1/jetsoninstaller-r39.2.1-2026-08-07-18-30-47-arm64.iso
sudo dd if="$ISO" of="$DEV" bs=4M conv=fsync oflag=direct status=progress
sudo cmp -n "$(stat -c%s "$ISO")" "$ISO" "$DEV" && echo "stick OK"
```

A forum user fixed an install that hung mid-way by rewriting the stick
([post #29](https://forums.developer.nvidia.com/t/jetpack-7-2-jetson-linux-r39-2-on-jetson-orin-nano-developer-kit-getting-started-and-feedback-thread/372151/29)),
so do the `cmp`.

For a keyboard-free stick for one robot, use
`isaac_ros_common/scripts/usb_installer/make_installer_usb.sh --robot <name>
--iso "$ISO" --out ~/<name>.iso --dev <stick>`. It runs on Arch or macOS
(`brew install xorriso`; the stick is `/dev/diskN` from
`diskutil list external`) and does the `cmp` itself. macOS won't mount a
USB stick's EFI partition without root, so a failed mount there proves
nothing about the stick.

## 3. Flash (at the board)

From the [Orin Nano quick start](https://docs.nvidia.com/jetson/orin-nano-devkit/user-guide/latest/quick_start.html).

1. Firmware gate: press Esc at the NVIDIA splash and read the version
   line (must be 36.0 or later).
2. Power off. Plug in the DP monitor, keyboard, Ethernet and the stick,
   leaving the NVMe in place. Apply power.
3. Press Esc at the NVIDIA logo, then Boot Manager, then the USB disk. Pick
   it explicitly; auto-boot times out on the capsule step
   ([post #8](https://forums.developer.nvidia.com/t/jetpack-7-2-jetson-linux-r39-2-on-jetson-orin-nano-developer-kit-getting-started-and-feedback-thread/372151/8)).
4. **Press Y at the firmware update prompt.** It waits 30 s. If you miss
   it, the install fails later; start over.
5. The UEFI capsule update runs in two passes and may reboot between them.
   Wait for both.
6. At the GRUB menu pick "Install Jetson ISO r39.2.1", choose the NVMe
   (`nvme0n1`, about 500 GB), confirm the erase, wait, reboot.
7. Pull the stick when told. oem-config: accept the EULA, then set username
   `nano-dev`, computer name `ts-nano-dev` (the laptop's `~/.ssh/config`
   has `Host ts-nano-dev`, `User nano-dev`) and connect the network.

If the installer dies at "Step 9/13 Updating boot firmware" with
`command_34 ... nvidia-l4t-bootloader ... exit status 100`, press Enter for
the shell and run `journalctl --no-pager | grep -B5 -A40 nvidia-l4t-bootloader`.
A "does not match any known boards" line is the board-spec bug from
[post #102](https://forums.developer.nvidia.com/t/jetpack-7-2-jetson-linux-r39-2-on-jetson-orin-nano-developer-kit-getting-started-and-feedback-thread/372151/102).
Someone on an Orin Nano Super with NVMe hit this on 2026-09-18
([post #118](https://forums.developer.nvidia.com/t/jetpack-7-2-jetson-linux-r39-2-on-jetson-orin-nano-developer-kit-getting-started-and-feedback-thread/372151/118))
and it was unresolved at the time. Save the journal to a spare stick and
stop there.

### If picking the USB disk drops straight back to the boot menu

Hero hit this 2026-10-01 (firmware 36.4.7, its old JetPack 6 install
trimmed). The stick is fine: its `bootaa64.efi` is NVIDIA's L4TLauncher,
which chose recovery boot, found no recovery partition and returned. Check
first, before picking the stick, so the normal path (with the Y firmware
prompt) works. Boot menu → UEFI Shell (don't run `map`, it scrolls off):

```
dmpstore Rootfs* -guid 781E084C-A330-417C-B678-38E696380CB9
```

Hero had `RootfsStatusSlotA` = `FF` (Unbootable; `00` is Normal) with
`RootfsRedundancyLevel` 0, so the launcher always forces recovery
(`ValidateRootfsStatus` in `edk2-nvidia`). Probably the trimmed JetPack 6
system never marked its boots good and used up the 3 retries. Fix:

```
setvar RootfsStatusSlotA -guid 781E084C-A330-417C-B678-38E696380CB9 -nv -rt -bs =00000000
```

Also Setup → Device Manager → NVIDIA Configuration → L4T Configuration:
**L4T Boot Mode** must be Application Default (hero's was Recovery
Partition). F10 there fails with "Submit Fail For Form: Grace
Configuration"; press D and the L4T change still saves.

What hero did instead, before the slot fix was known: from the shell,
`FSn:\EFI\BOOT\grubaa64.efi` (FSn: the one whose `EFI\BOOT` lists
`bootaa64`, `grubaa64`, `mmaa64`, `shimaa64`). The install works, but it
skips the firmware update: the installer logs "Using ISO to update the
QSPI version 2360327 is not supported", so 36.4.7 firmware stays under
R39. Hero then booted recovery (black screen) until the `setvar` above.
The firmware update then went in from Linux, the same capsule-on-disk the
launcher stages (board `jetson-orin-nano-devkit-super` →
`TEGRA_BL_3767_super.Cap`, from the stick's ESP):

```bash
sudo mkdir -p /boot/efi/EFI/UpdateCapsule
sudo cp <stick ESP>/EFI/TEGRA_BL_3767_super.Cap /boot/efi/EFI/UpdateCapsule/TEGRA_BL.Cap
V=/sys/firmware/efi/efivars/OsIndications-8be4df61-93ca-11d2-aa0d-00e098032b8c
sudo chattr -i $V
printf "\x07\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00" | sudo dd of=$V bs=12
sudo reboot   # applies it; nvbootctrl dump-slots-info then says 39.2.1
```

The two "Ubuntu" boot entries the installer adds point at `\EFI\ubuntu`,
which isn't on the ESP; they bounce and are harmless. Over USB-C the
serial console (`/dev/cu.usbmodem*`, login prompt on `ttyGS0`) works from
the first boot. The network link to a Mac only works once
`jetson_setup.sh` has bridged NCM (NVIDIA's start script never brings up
`usb1`). It runs at USB 2.0 (36 MB/s) with Apple's cable and port: the
device controller's SuperSpeed phy is `usb3-0`, whose companion is
`usb2-1`, not the USB-C port's `usb2-0` (hero's device tree; not checked
against the schematic). Use Ethernet on the Mac's switch for anything big
(108 MB/s measured). Photos
and videos: `~/robot-flash-logs/hero-2026-10-01/` on the Mac mini.

First checks on the board:

```bash
cat /etc/nv_tegra_release        # R39 (release), REVISION: 2.1
uname -r                         # 6.8.x
cat /etc/nv_boot_control.conf    # TNSPEC should end in ...-super-...
sudo nvpmodel -q; grep POWER_MODEL /etc/nvpmodel.conf
```

7.2.1's ISO flashes the Super config by default
([JetsonHacks](https://jetsonhacks.com/2026/08/12/jetpack-7-2-1-released/)).
On 7.2.0 some boards came up with only 7 W and 15 W modes
([post #6](https://forums.developer.nvidia.com/t/jetpack-7-2-jetson-linux-r39-2-on-jetson-orin-nano-developer-kit-getting-started-and-feedback-thread/372151/6)).
If MAXN_SUPER isn't in the list, note it and move on; it doesn't block
step 1. If it is, select it (top-bar power menu, or
`sudo nvpmodel -m <id>` with the id from `nvpmodel.conf`) and run
`sudo jetson_clocks`, as the Isaac ROS guide asks.

## 4. Make it reachable again

```bash
sudo apt update && sudo apt install -y openssh-server
sudo systemctl enable --now ssh
```

Passwordless sudo, so agents and scripts can run `sudo -n`, and the
timezone. The r39.2.1 image ships `/etc/timezone` as `Etc/UTC` and oem-config
only sets `/etc/localtime`, so anything reading the zone name from
`/etc/timezone` (Python's `tzlocal`, Java) sees UTC:

```bash
echo "nano-dev ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/90-nano-dev-nopasswd && sudo chmod 440 /etc/sudoers.d/90-nano-dev-nopasswd
sudo timedatectl set-timezone America/New_York && echo America/New_York | sudo tee /etc/timezone
```

Add the laptop's public key to the new account with
`ssh-copy-id <user>@<board-ip>` from the laptop.

Join Tailscale as a new node (substitute the board's hostname):

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --hostname <name> --advertise-tags=tag:jetsons
sudo tailscale set --ssh
tailscale ip -4
```

Put the new IP in `fastdds_cable.xml` and `fastdds_udp_only.xml`, and
configure Wi-Fi again if needed.
Campus DNS registers the board's Wi-Fi hostname, so the short name can
resolve to the Wi-Fi address, where port 22 is blocked. Give `~/.ssh/config`
the tailscale IP as `HostName` (ts-nano-sentry, 2026-09-30).

From the laptop: `ssh ts-nano-dev true`. If it warns about a changed host
key after the reflash, confirm it is the intended board, then remove its
old entry with `ssh-keygen -R ts-nano-dev` and reconnect.

## 5. Kernel 6.8 hardware checks (host, no container)

Record results in [hardware status](JAZZY_PLAN.md#hardware-status).

```bash
# DJI serial bridge UART: check ttyTHS1 and its *.serial address
for t in /sys/class/tty/ttyTHS*; do echo "$t -> $(readlink -f $t/device)"; done
ls -l /dev/ttyTHS1; groups | grep -w dialout || sudo usermod -aG dialout $USER
systemctl status nvgetty 2>/dev/null | head -3    # must not own the port
# loopback: jumper 40-pin header pins 8 and 10, then
stty -F /dev/ttyTHS1 115200 raw -echo; (timeout 2 cat /dev/ttyTHS1 &); sleep 0.5; echo ping > /dev/ttyTHS1

# RPLIDAR (CP210x, 10c4:ea60)
lsusb | grep -i 10c4:ea60; sudo dmesg | grep -i cp210x; ls -l /dev/ttyUSB*

# RealSense (8086:*), on a USB 3 port
lsusb | grep -i 8086; lsusb -t | grep -B1 -i uvc; ls -l /dev/video*; sudo dmesg | grep -iE 'uvcvideo|realsense' | tail
```

Pass: `ttyTHS1` maps to the intended UART and the loopback prints `ping`; the lidar appears as `/dev/ttyUSB0`; the RealSense
shows as a UVC device at 5000M. A full `rs-enumerate-devices` needs the
realsense image layer, built in section 8.

## 6. Docker, NVIDIA container toolkit, Isaac ROS CLI

Order follows the [Isaac ROS 4.6 getting started](https://nvidia-isaac-ros.github.io/v/release-4.6/getting_started/index.html)
page. Its Jetson steps are written for AGX Orin; the Orin Nano docs cover
Docker.

JetPack components ("Install via apt"; [Orin Nano JetPack setup](https://docs.nvidia.com/jetson/orin-nano-devkit/user-guide/latest/setup_jetpack.html)):

```bash
sudo apt update && sudo apt install -y nvidia-jetpack
```

Locale and apt prerequisites:

```bash
sudo apt install -y locales && sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 && export LANG=en_US.UTF-8
sudo apt install -y curl gnupg software-properties-common && sudo add-apt-repository -y universe
```

Isaac ROS apt repo. On Jetson the suite is `noble-jetpack`, not `noble`
(`noble` is the x86 line). `release-4` tracks the latest 4.x;
`release-4.6` pins the minor version:

```bash
k="/usr/share/keyrings/nvidia-isaac-ros.gpg"
curl -fsSL https://isaac.download.nvidia.com/isaac-ros/repos.key | sudo gpg --dearmor \
    | sudo tee -a $k > /dev/null
f="/etc/apt/sources.list.d/nvidia-isaac-ros.list"
sudo touch $f
s="deb [signed-by=$k] https://isaac.download.nvidia.com/isaac-ros/release-4 noble-jetpack main"
grep -qxF "$s" $f || echo "$s" | sudo tee -a $f
sudo apt-get update
sudo apt-get install -y isaac-ros-cli
```

Docker and the container toolkit ([Orin Nano Docker setup](https://docs.nvidia.com/jetson/orin-nano-devkit/user-guide/latest/setup_docker.html)):

```bash
sudo apt install -y nvidia-container curl jq
curl https://get.docker.com | sh
sudo nvidia-ctk runtime configure --runtime=docker
sudo jq '. + {"default-runtime": "nvidia"}' /etc/docker/daemon.json | sudo tee /etc/docker/daemon.json.tmp
sudo mv /etc/docker/daemon.json.tmp /etc/docker/daemon.json
sudo systemctl daemon-reload && sudo systemctl restart docker
sudo usermod -aG docker $USER
newgrp docker        # opens a new shell with the group; or log out and back in
```

Pre-flight (Isaac ROS guide):

```bash
docker info | grep -E "Runtimes|Default Runtime"     # nvidia listed and default
docker run --rm hello-world
docker run --rm --gpus all ubuntu:24.04 bash -lc 'echo "NVIDIA runtime OK"'
```

Initialise the CLI and a workspace. Jazzy machines use domain 1 until
cutover (`JAZZY_PLAN.md`, What still has to be checked on hardware):

```bash
sudo isaac-ros init docker
mkdir -p ~/workspaces/isaac_ros-dev/src
echo 'export ISAAC_ROS_WS="${ISAAC_ROS_WS:-${HOME}/workspaces/isaac_ros-dev/}"' >> ~/.bashrc
echo 'export ROS_DOMAIN_ID=1' >> ~/.bashrc
source ~/.bashrc
```

Get the ONNX from the source linked in the
[hardware checklist](JAZZY_PLAN.md#hardware-checklist) and place it in
`~/workspaces/isaac_ros-dev/isaac_ros_assets/models/yolo11/`. Don't clone
our repo or add image keys yet; that is section 8.

## 7. Done check

```bash
isaac-ros activate
```

It pulls the prebuilt `nvcr.io/nvidia/isaac/ros` image (several GB) and
drops you in a shell in `isaac_ros_dev_container`. Inside:

```bash
cat /etc/os-release | grep VERSION=        # 24.04
echo $ROS_DISTRO $ROS_DOMAIN_ID            # jazzy 1
tegrastats --interval 1000                 # prints a line a second; Ctrl-C
```

The CLI bind-mounts the host's `/usr/bin/tegrastats` and `/sys/kernel/debug`
into the container on aarch64
([`run_dev.py`, release-4.6](https://github.com/NVIDIA-ISAAC-ROS/isaac-ros-cli/blob/release-4.6/scripts/run_dev/run_dev.py)),
so a "not found" here means the host binary is missing, not the image.

Optional GPU check, if the ONNX is in place (it is step 5's engine build
anyway):

```bash
/usr/src/tensorrt/bin/trtexec --onnx=$ISAAC_ROS_WS/isaac_ros_assets/models/yolo11/<model>.onnx --fp16 --saveEngine=/tmp/test.plan
```

`CUDA failed to initialize ... error 801` is the failure an AGX Orin user
reported on 7.2.1 in containers
([post #115](https://forums.developer.nvidia.com/t/jetpack-7-2-jetson-linux-r39-2-on-jetson-orin-nano-developer-kit-getting-started-and-feedback-thread/372151/115)).
Record it and stop.

The stock image works when `activate` starts it and `tegrastats` prints
inside it. Exit the container before section 8.

## 8. Our image

```bash
cd ~/workspaces/isaac_ros-dev
git clone --recurse-submodules https://github.com/Thornbots/thornbots_workspace.git src
cd src && git submodule foreach --recursive \
  'git checkout $(git config -f $toplevel/.gitmodules submodule.$name.branch)'
isaac_ros_common/scripts/setup_workspace.sh
export ISAAC_ROS_WS=~/workspaces/isaac_ros-dev
isaac-ros activate --build-local
```

`activate` exits 0 even when a layer fails, so read its output. In a second
shell, count the layers against overlay2's ~128 cap and run the smoke test:

```bash
docker image inspect -f '{{len .RootFS.Layers}}' \
  $(docker inspect -f '{{.Config.Image}}' isaac_ros_jazzy_container)
~/workspaces/isaac_ros-dev/src/.claude/skills/isaac-ros-docker/smoke.sh
```

Step 1 is done when our image starts on the Orin and `smoke.sh` passes. Put
the kernel 6.8 check results, the power modes offered, the layer count and
the image size in the commit message that records step 1.
