'use strict';

var Blog = require(
    '../../page_objects/page_blog.js'
  );

describe( 'Pagination', function() {
  var page;

  beforeEach( function() {
    page = new Blog();
    page.get();
  } );

  it( 'should navigate to the first page of filtered results', function() {
    page.searchFilterBtn.click();
    browser.sleep( 1000 );

    page.searchCategoryLabel.click();
    page.searchFilterSubmitBtn.click();
    browser.sleep( 1000 );

    expect( browser.getCurrentUrl() ).not.toContain( 'page=' );
    expect( browser.getCurrentUrl() ).toContain( 'at-the-cfpb' );
  } );

  it( 'should navigate to the second filtered page', function() {
    page.searchFilterBtn.click();
    browser.sleep( 1000 );

    page.searchCategoryLabel.click();
    page.searchFilterSubmitBtn.click();
    browser.sleep( 1000 );

    page.paginationNextBtn.click();
    browser.sleep( 1000 );

    expect( browser.getCurrentUrl() ).toContain( 'page=2' );
    expect( browser.getCurrentUrl() ).toContain( 'at-the-cfpb' );
  } );

  it( 'should navigate to the fifth filtered page', function() {
    page.searchFilterBtn.click();
    browser.sleep( 1000 );

    page.searchCategoryLabel.click();
    page.searchFilterSubmitBtn.click();
    browser.sleep( 1000 );

    var input = browser.element( by.css( '#m-pagination_current-page' ) );
    var btn = browser.element( by.css( '#m-pagination_submit-btn' ) );

    input.clear().sendKeys( '5' );
    btn.click();
    browser.sleep( 1000 );

    expect( browser.getCurrentUrl() ).toContain( 'page=5' );
    expect( browser.getCurrentUrl() ).toContain( 'at-the-cfpb' );
  } );
} );
