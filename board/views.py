from django.http import Http404
from django.shortcuts import render, redirect
from member.models import BoardMember
from .models import Board
from .forms import BoardForm
from django.core.paginator import Paginator
# Create your views here.

def board_list(request):
    all_boards  = Board.objects.all().order_by('-id')
    # 변수명을 all_boards 로 바꿔주었다.
    page        = int(request.GET.get('p', 1))
    # p라는 값으로 받을거고, 없으면 첫번째 페이지로
    pagenator   = Paginator(all_boards, 10)
    # Paginator 함수를 적용하는데, 첫번째 인자는 위에 변수인 전체 오브젝트, 2번째 인자는
    # 한 페이지당 오브젝트 2개씩 나오게 설정
    boards      = pagenator.get_page(page)
    # 처음 2개가 세팅 된다.
    return render(request, 'board_list.html', {"boards":boards})


def board_write(request):
    if not request.session.get('user'):
        return redirect('/member/login/')
    # 세션에 'user' 키를 불러올 수 없으면, 로그인하지 않은 사용자이므로 로그인 페이지로 리다이렉트 한다.
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            user_id         = request.session.get('user')
            member          = BoardMember.objects.get(pk=user_id)

            board = Board()
            board.title     = form.cleaned_data['title']
            board.contents  = form.cleaned_data['contents']
            board.writer    = member
            board.save()
            return redirect('/board/list/')
    else:
        form = BoardForm()
    return render(request, 'board_write.html', {'form':form})



def board_detail(request, pk):
        try:
            board = Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            raise Http404('게시글을 찾을 수 없습니다')
            # 게시물의 내용을 찾을 수 없을 때 내는 오류 message.

        return render(request, 'board_detail.html', {'board': board})


